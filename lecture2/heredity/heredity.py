import csv
import itertools
import sys
import random

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
    print(people)

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
    with open(filename) as f:
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
    # build dict with structure info about each person
    info = {p: {"genes": 0, "has_trait": False, "has_parents": False} for p in people}
    for p in people:
        if p in one_gene:
            info[p]["genes"] = 1
        elif p in two_genes:
            info[p]["genes"] = 2
        if p in have_trait:
            info[p]["has_trait"] = True
        if people[p]["mother"]:
            info[p]["has_parents"] = True
    print(f"people: {people}")
    print(f"info: {info}")

    # set joint probability
    joint_prob = 1

    # get joint probabilities for every person
    for p in people:
        print(f"person {p}")
        # check for parents
        if info[p]["has_parents"]:
            # get probability of both parents to pass down gene
            father_prob = probablity_to_pass_gene(people[p]["father"], info)
            mother_prob = probablity_to_pass_gene(people[p]["mother"], info)     
            if info[p]["genes"] == 0:
                # when there are supposed to be 0 genes we need the probability that both parents DO NOT pass it down
                joint_prob_temp = (1 - father_prob) *  (1 - mother_prob)
            elif info[p]["genes"] == 1:
                # when there are supposed to be 1 genes we need the probability that ONE OF the parents pass it down
                joint_prob_temp = father_prob * (1 - mother_prob) + mother_prob * (1 - father_prob)
            else:
                # when there are supposed to be 2 genes we need the probability that BOTH PARENTS do pass it down
                joint_prob_temp = father_prob * mother_prob
        else:
            # get probability to have X genes
            gene_prob = PROBS["gene"][info[p]["genes"]]
            # get probablity to have trait with X genes
            trait_prob = PROBS["trait"][info[p]["genes"]][info[p]["has_trait"]]
            # get joint probablity of both
            joint_prob_temp = gene_prob * trait_prob
        # add new factor to final joint probability
        joint_prob = joint_prob * joint_prob_temp 

    return joint_prob


def probablity_to_pass_gene(person, info):
    """
    Helper to return the probability to pass on the gene.

    1 - "passing probability" ca be used conversely
    """
    genes = info[person]["genes"]
    if genes == 0:
        # probability to pass on gene is 0
        passing_prob = 0 + PROBS["mutation"]
    elif genes == 1:
        # probability to pass on gene is 0.5
        passing_prob = 0.5 - PROBS["mutation"]
    else:
        # probability to pass on gene is 1
        passing_prob = 1 - PROBS["mutation"]

    return passing_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    print(f"probabilities at start: {probabilities}")
    # iterate over people
    for p in probabilities:
        if p in one_gene:
            probabilities[p][1] = p
        elif p in two_genes:
            probabilities[p][2] = p
        else:
            probabilities[p][0] = p
        if p in have_trait:
            probabilities[p]["trait"][True] = p
        else:
            probabilities[p]["trait"][False] = p
    
    return probabilities
       


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
