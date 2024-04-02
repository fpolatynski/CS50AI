import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    # Prepare dict for probability distribution
    distribution = {}
    # Number of values
    n = len(corpus)
    # Probability of random chose
    d = 1 - damping_factor
    # Set random probability
    for p in corpus.keys():
        distribution[p] = d / n
    # Number of page links
    dn = len(corpus[page])
    # Set probability of linked values
    if dn > 0:
        # if page link other pages
        for p in corpus[page]:
            distribution[p] += damping_factor/dn
    else:
        # if page doesn't link any
        for p in corpus.keys():
            distribution[p] = damping_factor / n

    # return distribution
    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Prepare dict for distribution
    distribution = {}
    # Chose random page to start
    current_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        dist = transition_model(corpus, current_page, damping_factor)
        #
        r = random.random()
        # Get new page from distribution
        for p, d in dist.items():
            if r <= d:
                current_page = p
                break
            else:
                r -= d

        distribution[current_page] = distribution.get(current_page, 0) + 1/n
    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dist = {}
    n = len(corpus)
    # Set all ranks to same value
    for x in list(corpus.keys()):
        dist[x] = 1/n

    while True:
        i = 0
        # Count new values fo every probability that changes
        to_remove = set()
        for page in corpus.keys():
            # create list of pages that leads to page
            parents = []
            for p0, p1 in corpus.items():
                if page in p1:
                    parents.append(p0)
            new_p = (1 - damping_factor)/len(corpus) + damping_factor * sum([dist[x]/len(corpus[x]) for x in parents])

            if abs(new_p - dist[page]) < 0.00001:
                i += 1
            else:
                dist[page] = new_p

        if i == n:
            break
    return dist


if __name__ == "__main__":
    main()
