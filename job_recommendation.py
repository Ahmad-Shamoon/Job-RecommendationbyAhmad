import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

job_data = { 'job_title' : ['Data Scientist', 'Web Developer', 'Machine Learning Engineer','Data Analyst', 'Backend Developer'],
             'job_description' : [
                'Looking for a Data Scientist with skills in Python, Machine Learning, and SQL.',
                'Need a Web Developer experienced in JavaScript, HTML, CSS, and React.',
                'Hiring Machine Learning Engineer with expertise in Python, TensorFlow, and deep learning.',
                'Data Analyst required with skills in Python, SQL, data visualization, and Excel.',
                'Backend Developer position for someone skilled in Java, Spring Boot, and databases.'],
             'skills-required' : ['Python, Machine Learning, SQL',
                                  'JavaScript, HTML, CSS, React',
                                  'Python, TensorFlow, Deep Learning',
                                  'Python, SQL, Data Visualization, Excel',
                                  'Java, Spring Boot, Databases']}

user_data = { 'user skills': ['Python, SQL, Machine Learning'],
              'Experience': [3],
              'Preferred Location': ['Remote']}

jobs_df = pd.DataFrame(job_data)
user_df = pd.DataFrame(user_data)
tfidf = TfidfVectorizer(stop_words='english')


combined_text = pd.concat([jobs_df['job_description'], user_df['user skills']])
tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit(combined_text)
job_tfidf_matrix = tfidf.transform(jobs_df['job_description'])
user_tfidf_matrix = tfidf.transform(user_df['user skills'])

cosin_sim = cosine_similarity(job_tfidf_matrix, user_tfidf_matrix)

top_job_indices = cosin_sim.argsort()[0][-3:]
recommended_jobs = jobs_df.iloc[top_job_indices][['job_title', 'job_description']]
print("Top 3 Job Recommendations:")
print(recommended_jobs)

def get_user_input():
    user_skills = input('Enter your skills (comma seperated): ')
    uer_experience = int(input('Enter your experience: '))
    user_preferrence = input('Enter your preferred job location: ')

    new_user_profile = {'user skills': [user_skills],
                        'experience': [uer_experience],
                        'job preferrence': [user_preferrence]}
    return  pd.DataFrame(new_user_profile)
new_user_df = get_user_input()

new_user_tfidf_matrix = tfidf.transform(new_user_df['user skills'])

# Calculate cosine similarity between new user and job postings
new_cosine_sim = cosine_similarity(new_user_tfidf_matrix, job_tfidf_matrix)

# Get top 3 job recommendations for the new user
new_top_job_indices = new_cosine_sim.argsort()[0][-3:]  # Get indices of top 3 similar jobs

# Display recommended jobs for the new user
new_recommended_jobs = jobs_df.iloc[new_top_job_indices][['job_title', 'job_description']]
print("\nRecommended Jobs for You:")
print(new_recommended_jobs)