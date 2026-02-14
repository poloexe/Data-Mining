import itertools

# The Dataset
transactions = [
    ['Bread', 'Milk'],
    ['Bread', 'Diaper', 'Beer', 'Eggs'],
    ['Milk', 'Diaper', 'Beer', 'Coke'],
    ['Bread', 'Milk', 'Diaper', 'Beer'],
    ['Bread', 'Milk', 'Diaper', 'Coke']
]

min_support = 0.60    # 60%
min_confidence = 0.70 # 70%
total_transactions = len(transactions)

print(f"--- Processing {total_transactions} Transactions ---")

# Helper Function: Count Support
def get_support(itemset):
    count = 0
    for row in transactions:
        # Check if the 'itemset' is inside this row
        if set(itemset).issubset(set(row)):
            count += 1
    return count

# Find Frequent Itemsets
print(f"\n[1] Frequent Itemsets (Min Support: {min_support*100}%)")
print(f"    (Itemset must appear in at least {min_support * total_transactions} transactions)")

all_items = sorted(list(set(item for sublist in transactions for item in sublist)))
frequent_itemsets = [] # To store valid itemsets for step 4

# Check sizes 1 to 3
for size in range(1, 4):
    combinations = itertools.combinations(all_items, size)
    
    for itemset in combinations:
        count = get_support(itemset)
        support = count / total_transactions
        
        if support >= min_support:
            frequent_itemsets.append(itemset)
            print(f"- {itemset}: Found {count} times (Support: {support:.0%})")

# Generate Rules
print(f"\n[2] Association Rules (Min Confidence: {min_confidence*100}%)")

# Look at every frequent itemset with more than 1 item
for itemset in frequent_itemsets:
    if len(itemset) > 1:
        # Generate all possible rules A -> B from this itemset
        # e.g., if itemset is {Milk, Bread}, we check Milk->Bread and Bread->Milk
        permutations = itertools.permutations(itemset)
        
        for perm in permutations:
            # Split permutation into Antecedent (A) -> Consequent (B)
            # We try splitting at every possible point
            for i in range(1, len(perm)):
                antecedent = perm[:i]
                consequent = perm[i:]
                
                # Calculate metrics
                support_both = get_support(itemset) / total_transactions
                support_antecedent = get_support(antecedent) / total_transactions
                
                confidence = support_both / support_antecedent
                
                # Check threshold
                if confidence >= min_confidence:
                    lift = confidence / (get_support(consequent) / total_transactions)
                    
                    # Print clearly
                    ant_str = ", ".join(antecedent)
                    con_str = ", ".join(consequent)
                    print(f"Rule: If [{ant_str}] -> Then [{con_str}]")
                    print(f"    Conf: {confidence:.0%} | Lift: {lift:.2f}")

print("\nDone.")