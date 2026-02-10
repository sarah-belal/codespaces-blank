from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)  # For reproducible data

# Generate Members
def generate_members(n=1000):
    members = []
    for i in range(n):
        members.append({
            'member_id': f'MEM-{i+1:05d}',
            'name': fake.name(),
            'age': random.randint(18, 80),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'zip_code': fake.zipcode()
        })
    return pd.DataFrame(members)

# Generate Claims
def generate_claims(n=10000):
    claims = []
    statuses = ['APPROVED', 'DENIED', 'PENDING', 'UNDER_REVIEW']
    claim_types = ['MEDICAL', 'DENTAL', 'VISION', 'PHARMACY', 'MENTAL_HEALTH']
    
    for i in range(n):
        claim_date = fake.date_between(start_date='-2y', end_date='today')
        status = random.choice(statuses)
        
        claims.append({
            'claim_id': f'CLM-{i+1:05d}',
            'member_id': f'MEM-{random.randint(1, 1000):05d}',
            'claim_date': claim_date,
            'claim_type': random.choice(claim_types),
            'claim_amount': round(random.uniform(50, 15000), 2),
            'status': status,
            'processed_date': claim_date + timedelta(days=random.randint(1, 30)) if status != 'PENDING' else None,
            'provider_name': fake.company()
        })
    return pd.DataFrame(claims)

# Generate Policies
def generate_policies(n=1000):
    policies = []
    plan_types = ['PPO', 'HMO', 'EPO', 'POS']
    
    for i in range(n):
        policies.append({
            'policy_id': f'POL-{i+1:05d}',
            'member_id': f'MEM-{i+1:05d}',
            'plan_type': random.choice(plan_types),
            'premium': round(random.uniform(200, 1500), 2),
            'deductible': random.choice([500, 1000, 2000, 5000]),
            'effective_date': fake.date_between(start_date='-3y', end_date='-1y')
        })
    return pd.DataFrame(policies)

if __name__ == "__main__":
    print("Generating data...")
    
    # Generate datasets
    members_df = generate_members(1000)
    claims_df = generate_claims(10000)
    policies_df = generate_policies(1000)
    
    # Save to CSV
    members_df.to_csv('members.csv', index=False)
    claims_df.to_csv('claims.csv', index=False)
    policies_df.to_csv('policies.csv', index=False)
    
    print(f"Generated {len(members_df)} members")
    print(f"Generated {len(claims_df)} claims")
    print(f"Generated {len(policies_df)} policies")
    print("\nFiles created: members.csv, claims.csv, policies.csv")