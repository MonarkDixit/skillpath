#src/data_loader.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose: 
#1. Loads and audits the LinkedIn Job Posting 2023 dataset.
#2. Joins postings.csv with job_skills.csv and the skills lookup to produce a clean mapping of
                                                        #role title -> list of required skills. 
#3. Also computes frequency rankings of skills pre role for the UI.

import pandas as pd
import os
from collections import defaultdict, Counter

#--------------------------------------------------------------------
#File Paths

DATA_DIR = "data"
POSTINGS_PATH = os.path.join(DATA_DIR, "postings.csv")
JOB_SKILLS_PATH = os.path.join(DATA_DIR, "jobs", "job_skills.csv")
SKILLS_LOOKUP_PATH = os.path.join(DATA_DIR, "mappings", "skills.csv")

#--------------------------------------------------------------------
#Load Raw Files

def load_postings():
    """
    Loads postings.csv and returns a DataFrame with job_id and job_title columns. 
    Drops rows where title is missing since we need the role name.
    """
    df = pd.read_csv(POSTINGS_PATH, usecols=["job_id", "title"])  #Only load relevant columns to save memory
    df = df.dropna(subset=["title"])            #Drop rows where title is missing since we need the role name
    df["title"] = df["title"].astype(str).str.strip().str.lower()  #Remove leading/trailing whitespace
    return df

def load_job_skills():
    """
    Loads job_skills.csv which maps job_id to skill_abr (skills abbreviation). 
    Returns a DataFrame with job_id and skill_abr columns.
    """
    df = pd.read_csv(JOB_SKILLS_PATH)
    df = df.dropna()  #Only load relevant columns to save memory
    return df

def load_skills_lookup():
    """
    Loads skills.csv which maps skill_abr to skill_name. 
    Returns a dict of {skill_abr: skill_name}.
    """
    df = pd.read_csv(SKILLS_LOOKUP_PATH)
    df = df.dropna()  
    #Build a lookup dict for O(1) skill name resolution
    return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

#--------------------------------------------------------------------
#Build Role to Skills Mapping

def build_role_skills_map():
    """
    Joins postings, job_skills, and skills lookup to produce to produce a clean dict mapping
    each role title to a list of required skill names.

    Returns:
        dict: {role_title(str): [skill_name, skill_name, ...]} 
    """
    postings = load_postings()              #DataFrame with job_id and title
    job_skills = load_job_skills()          #DataFrame with job_id and skill_abr
    skills_lookup = load_skills_lookup()    #Dict with skill_abr -> skill_name mapping

    #Merge postings with job_skills on job_id to get role title and skill_abr in the same DataFrame
    merged = pd.merge(postings, job_skills, on="job_id", how="inner")

    #Map skill abbreviations to full skill names using the lookup dict
    skill_col = merged.columns[-1]
    merged["skill_name"] = merged[skill_col].map(skills_lookup)
    merged = merged.dropna(subset=["skill_name"])
    merged["skill_name"] = merged["skill_name"].str.strip().str.lower()

    #Group by role title and collect all skills for that role
    role_skills = defaultdict(list)
    for _, row in merged.iterrows():
        role_skills[row["title"]].append(row["skill_name"])

    return dict(role_skills)


def get_top_skills_for_role(role_skill_map: dict, role: str, top_n: int = 15):
    """
    Returns the top N most frequently required skills for a given role.

    Args:
        role_skill_map (dict): Output of build_role_skill_map()
        role (str): Role title 
        top_n (int): Number of top skills to return

    Returns:
        list of (skill_name, count) tuples sorted by frequency in descending order.
    """
    
    skills = role_skill_map.get(role.lower(), [])   
    return Counter(skills).most_common(top_n)

def get_all_roles(role_skill_map: dict):
    """
    Returns a list of all unique role titles in the dataset.
    Used to populate the dropdown menu in the UI.
    """
    return sorted(role_skill_map.keys())        

def get_all_skills(role_skill_map: dict):
    """
    Returns a set of all unique skill names in the dataset.
    Used to populate the dropdown menu in the UI.
    """
    all_skills = set()
    for skills in role_skill_map.values():
        all_skills.update(skills)
    return sorted(all_skills)

#--------------------------------------------------------------------
#Audit Report

def audit_dataset():
    """
    Prints an audit report of the dataset including:
    - Total postings
    - Total unique roles
    - Total unique skills
    - Top 10 most common roles
    - Top 10 most common skills overall
    - Sample of role to skills mappings
    """
    print("-"*65)
    print(" SkillPath: Dataset Audit Report ")
    print("-"*65)

    postings = load_postings()          
    job_skills = load_job_skills()
    skills_lookup = load_skills_lookup()
    role_skills_map = build_role_skills_map()
    
    #Print summary statistics
    print(f"\n  Total job postings:        {len(postings):,}")
    print(f"  Total job-skill pairs:     {len(job_skills):,}")
    print(f"  Skills in lookup table:    {len(skills_lookup):,}")
    print(f"  Unique role titles:        {len(role_skills_map):,}")
    
    all_skills = get_all_skills(role_skills_map)
    print(f"  Unique skill (mapped):        {len(all_skills):,}")

    #Print top roles and skills
    print(f"\n  Top 10 Most Common Roles:")
    role_counts = Counter()
    for role, skills in role_skills_map.items():
        role_counts[role] += len(skills)
    for role, count in role_counts.most_common(10):
        print(f"    {role:<45} {count:>6} skill mentions")

    #Print top skills overall (not role specific)
    print(f"\n  Top 10 Most Common Skills Overall:")
    all_skill_list = []
    for skills in role_skills_map.values():
        all_skill_list.extend(skills)
    for skill, count in Counter(all_skill_list).most_common(10):
        print(f"    {skill:<45} {count:>6}")

    #Print sample role to skills mappings
    print(f"\n  SAMPLE ROLE TO SKILLS MAPPINGS (first 3 roles)")
    for i, (role, skills) in enumerate(list(role_skills_map.items())[:3]):
        unique_skills = list(set(skills))[:8]
        print(f"\n    Role: {role}")
        print(f"    Skills: {unique_skills}")

    print("\n" + "-" * 65)
    print("  Audit complete.")
    print("-" * 65)


#--------------------------------------------------------------------
#Entry Point

if __name__ == "__main__":
    audit_dataset()