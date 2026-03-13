import nltk
import re
from rake_nltk import Rake

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Tech indicators - if a word contains or matches these patterns, it's likely technical
TECH_PATTERNS = [
    r'^[a-z]+\d+',           # words with numbers: python3, k8s, s3
    r'^\w+\.\w+',            # dotted: node.js, asp.net
    r'^[a-z]+/[a-z]+',       # slashed: ci/cd, tcp/ip
    r'^\w+-\w+',             # hyphenated: well-known tools
]

# Known tech terms seed list (small, just for validation not full coverage)
TECH_SEED = {
    # Languages
    "python", "java", "javascript", "typescript", "golang", "go", "ruby",
    "bash", "powershell", "scala", "rust", "kotlin", "php", "swift",
    # Cloud
    "aws", "azure", "gcp", "ec2", "s3", "lambda", "eks", "ecs", "rds",
    "cloudformation", "terraform", "pulumi",
    # DevOps
    "docker", "kubernetes", "jenkins", "ansible", "helm", "argocd",
    "gitlab", "github", "bitbucket", "maven", "gradle", "nexus",
    # Monitoring
    "prometheus", "grafana", "datadog", "splunk", "elk", "kibana",
    "elasticsearch", "logstash", "newrelic", "dynatrace", "zabbix",
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb",
    "oracle", "sqlite", "kafka", "rabbitmq",
    # Networking & Security
    "nginx", "apache", "ssl", "tls", "dns", "vpn", "oauth", "jwt",
    "linux", "unix", "windows", "ubuntu", "centos", "debian",
    # Concepts
    "devops", "devsecops", "gitops", "sre", "cicd", "agile", "scrum",
    "microservices", "api", "rest", "graphql", "grpc", "serverless",
    # Frameworks
    "django", "fastapi", "flask", "spring", "react", "angular", "vue",
    "nodejs", "express", "tensorflow", "pytorch", "pandas", "numpy",
    # Certifications
    "cka", "ckad", "aws", "gcp", "ccna", "comptia",
}

# Words to always ignore regardless
IGNORE_WORDS = {
    "experience", "knowledge", "understanding", "ability", "abilities",
    "skill", "skills", "years", "team", "work", "working", "role",
    "position", "job", "company", "responsibilities", "requirements",
    "qualifications", "plus", "good", "strong", "excellent", "great",
    "including", "related", "relevant", "preferred", "required",
    "familiar", "proficient", "hands", "time", "basis", "field",
    "area", "level", "degree", "bachelor", "master", "communication",
    "problem", "solving", "management", "development", "candidate",
    "asset", "assets", "budget", "cost", "costs", "employee", "employees",
    "ensure", "establish", "collaborate", "collaboration", "environment",
    "enterprise", "digital", "dynamic", "efficient", "comprehensive",
    "essential", "comfortable", "communicative", "detailed", "detail",
    "closely", "along", "across", "within", "berlin", "dam", "admin",
    "coordinator", "manager", "engineer", "senior", "junior", "lead"
}


def is_tech_term(word: str) -> bool:
    # Check seed list
    if word in TECH_SEED:
        return True
    # Check tech patterns
    for pattern in TECH_PATTERNS:
        if re.match(pattern, word):
            return True
    return False


def extract_keywords(text: str) -> set:
    rake = Rake()
    rake.extract_keywords_from_text(text)
    phrases = rake.get_ranked_phrases()

    keywords = set()
    for phrase in phrases:
        words = phrase.lower().split()
        for word in words:
            clean = re.sub(r'[^a-z0-9/\.\-\+#]', '', word)
            if (len(clean) > 1
                    and clean not in IGNORE_WORDS
                    and is_tech_term(clean)):
                keywords.add(clean)

    return keywords


def get_missing_keywords(resume_text: str, jd_text: str) -> dict:
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched = sorted(jd_keywords & resume_keywords)
    missing = sorted(jd_keywords - resume_keywords)

    return {
        "total_jd_keywords": len(jd_keywords),
        "matched_keywords": matched,
        "matched_count": len(matched),
        "missing_keywords": missing,
        "missing_count": len(missing)
    }