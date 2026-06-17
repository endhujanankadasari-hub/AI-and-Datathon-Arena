def parse_job_description(job_description):
    return {"skills": ["Python", "SQL", "ML", "Cybersecurity"], "experience": 2}

def build_candidate_vector(candidate):
    return {
        "skills": candidate["skills"],
        "experience": candidate["experience"],
        "activity": candidate["activity"]
    }

def cosine_similarity(skills1, skills2):
    return len(set(skills1) & set(skills2)) / len(skills1)

def experience_fit(required, actual):
    return min(actual / required, 1.0)  # cap at 1.0

def activity_signal(activity):
    return 1.0 if activity else 0.0

def generate_explanation(jd_vector, candidate_vector):
    matched = set(jd_vector["skills"]) & set(candidate_vector["skills"])
    missing = set(jd_vector["skills"]) - set(candidate_vector["skills"])
    return f"Matched: {matched}, Missing: {missing}"

def rank_candidates(job_description, candidate_dataset):
    jd_vector = parse_job_description(job_description)
    ranked_candidates = []

    for candidate in candidate_dataset:
        candidate_vector = build_candidate_vector(candidate)
        
        similarity_score = cosine_similarity(jd_vector['skills'], candidate_vector['skills'])
        experience_score = experience_fit(jd_vector['experience'], candidate_vector['experience'])
        activity_score = activity_signal(candidate_vector['activity'])
        
        final_score = (similarity_score * 0.5) + (experience_score * 0.3) + (activity_score * 0.2)
        
        explanation = generate_explanation(jd_vector, candidate_vector)
        
        ranked_candidates.append({
            "candidate": candidate["name"],
            "score": final_score,
            "explanation": explanation
        })
    
    return sorted(ranked_candidates, key=lambda x: x["score"], reverse=True)

job_description = "Looking for a Data Scientist with Python, SQL, ML, and cybersecurity experience."

candidate_dataset = [
    {"name": "Alice", "skills": ["Python", "SQL", "Machine Learning"], "experience": 3, "activity": ["Kaggle"]},
    {"name": "Bob", "skills": ["Python", "Cybersecurity", "SQL"], "experience": 2, "activity": []}
]

ranked_list = rank_candidates(job_description, candidate_dataset)

# Print results nicely
for result in ranked_list:
    print(f"Candidate: {result['candidate']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Explanation: {result['explanation']}")
    print("-" * 40)
# updated new version 1.1