import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print("--------------------------------------------")
    print(f"PageRank Results from Sampling (n = {SAMPLES}):")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("--------------------------------------------")
    print(f"PageRank Results from Iteration:")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("--------------------------------------------")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    prob_dist = {}  # Probability distribution of which page to visitcl

    numlinks = len(corpus[page])  # Number of links on

    N = len(corpus)

    if corpus[page]:
        for link in corpus:  # Choose link from all pages in corpus
            prob_dist[link] = (1-damping_factor) / N
        for link in corpus[page]:  # Choose link from page
            prob_dist[link] += damping_factor / numlinks
    else:
        for link in corpus:
            prob_dist[link] = 1/N
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    page_rank_list = list()
    page = None

    for _ in range(n):
        # If no page, choose on eat random from corpus
        if page is None:
            page = random.choice(list(corpus.keys()))
            page_rank_list.append(page)
        else:  # If page exists, call transition model and use list of keys and values to compute randomly chosen samples.
            model = transition_model(corpus, page, damping_factor)
            sequence = list(model.keys())
            weight = list(model.values())
            page = random.choices(sequence, weight, k=1)[0]
            page_rank_list.append(page)
    for page in list(corpus.keys()):
        page_rank[page] = 1 / n * page_rank_list.count(page)  # Normalize pagerank and sum up to 1
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PR = dict()
    new_PR = dict()
    N = len(corpus)
    d = damping_factor
    threshold = 0.001

    # assign each page a rank of 1 / N, where N is the total number of pages in the corpus
    for page in corpus:
        PR[page] = 1 / N

    Flag = True

    while Flag:
        # repeatedly calculate new rank values based on all of the current rank values
        for page in PR:
            total = 0

            for i_pages in corpus:
                # check pages linking to current page
                if page in corpus[i_pages]:
                    total += PR[i_pages] / len(corpus[i_pages])
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if not corpus[i_pages]:
                    total += PR[i_pages] / N

            new_PR[page] = (1 - d) / N + d * total

        Flag = False

        # This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values.
        for page in PR:
            if abs(new_PR[page] - PR[page]) > threshold:
                Flag = True
            # update the rank values
            PR[page] = new_PR[page]

    return PR


if __name__ == "__main__":
    main()
