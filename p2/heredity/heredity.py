import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(f"data/{filename}.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def parent_genes(mother, father, one_gene, two_genes, child_genes):

    # Copies of genes a person gets
    mother_gene = 2 if mother in two_genes else 1 if mother in one_gene else 0
    father_gene = 2 if father in two_genes else 1 if father in one_gene else 0

    # the probability a child gets a copy from mother 
    prob_child_get_from_mother = mother_gene / 2
    # the probability a child gets a copy from father
    prob_child_get_from_father = father_gene / 2

    # the probability a child doesnt get a copy from mother/father
    not_from_mother = (prob_child_get_from_mother * PROBS["mutation"] + (1 - prob_child_get_from_mother) * (1 - PROBS["mutation"]))
    not_from_father = (prob_child_get_from_father * PROBS["mutation"] + (1 - prob_child_get_from_father) * (1 - PROBS["mutation"]))
    # the probability a child gets a copy from mother/father
    from_mother = (prob_child_get_from_mother * (1 - PROBS["mutation"]) + (1 - prob_child_get_from_mother) * PROBS["mutation"])
    from_father = (prob_child_get_from_father * (1 - PROBS["mutation"]) + (1 - prob_child_get_from_father) * PROBS["mutation"])
    

    # probability of child having gene depending on how many copies of gene
    if child_genes == 0:
        return not_from_mother * not_from_father
    elif child_genes == 1:
        return not_from_mother * from_father + from_mother * not_from_father
    elif child_genes == 2:
        return from_mother * from_father
    return 0
    
def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = 1
    
    # number of copies of gene a person has
    for person in people:
        child_genes = 2 if person in two_genes else 1 if person in one_gene else 0
    
        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        # if person has parents, calculate probabilites 
        if mother and father :
            prob *= parent_genes(mother, father, one_gene, two_genes, child_genes) 
        # For anyone with no parents listed in the data set,
        # use the probability distribution PROBS["gene"] to determine the probability that they have a particular number of the gene.         
        else:
            if child_genes == 0:
                prob *= PROBS["gene"][0]
            elif child_genes == 1:
                prob *= PROBS["gene"][1]
            elif child_genes == 2:
                prob *= PROBS["gene"][2]
        # calculate the probability that a person shows a certain trait
        prob *= PROBS["trait"][child_genes][trait]    
    return prob
    
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        child_genes = 2 if person in two_genes else 1 if person in one_gene else 0
        trait = person in have_trait
        probabilities[person]["gene"][child_genes] += p
        probabilities[person]["trait"][trait] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        sum_trait = 0
        sum_gene = 0
        for i in range(2):
            sum_trait += probabilities[person]["trait"][i]
        for i in range(2):
            probabilities[person]["trait"][i] /= sum_trait  
        for i in range(3):
            sum_gene += probabilities[person]["gene"][i]
        for i in range(3):
            probabilities[person]["gene"][i] /= sum_gene
     

if __name__ == "__main__":
    main()
