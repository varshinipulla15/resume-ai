import re

# Predefined technical keywords list
TECH_KEYWORDS = {
    # Cloud
    "aws", "azure", "gcp", "cloud", "ec2", "s3", "lambda", "cloudwatch",
    "cloudformation", "eks", "ecs", "rds", "vpc", "iam", "route53",

    # DevOps & CI/CD
    "docker", "kubernetes", "jenkins", "gitlab", "github", "bitbucket",
    "cicd", "ci/cd", "ansible", "terraform", "helm", "argocd", "spinnaker",
    "maven", "gradle", "nexus", "artifactory",

    # Monitoring & Logging
    "prometheus", "grafana", "elk", "elasticsearch", "logstash", "kibana",
    "datadog", "splunk", "newrelic", "dynatrace", "zabbix", "nagios",

    # Programming Languages
    "python", "java", "javascript", "typescript", "golang", "go", "ruby",
    "scala", "bash", "powershell", "groovy", "c++", "c#", "rust", "kotlin",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb",
    "oracle", "mssql", "sqlite", "elasticsearch", "neo4j", "kafka",

    # Networking & Security
    "linux", "unix", "nginx", "apache", "ssl", "tls", "dns", "http",
    "rest", "api", "microservices", "vpn", "firewall", "oauth", "jwt",

    # Frameworks & Libraries
    "django", "fastapi", "flask", "spring", "react", "angular", "vue",
    "nodejs", "express", "hibernate", "pandas", "numpy", "tensorflow",

    # Methodologies
    "agile", "scrum", "devops", "devsecops", "gitops", "sre", "kanban",
    "jira", "confluence", "sdlc", "tdd", "bdd",

    # Version Control
    "git", "svn", "mercurial",
}


def get_missing_keywords(resume_text: str, jd_text: str) -> dict:
    def extract_tech_words(text):
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#./]*\b', text.lower())
        # Only keep words that exist in our TECH_KEYWORDS list
        return set(words) & TECH_KEYWORDS

    jd_tech = extract_tech_words(jd_text)
    resume_tech = extract_tech_words(resume_text)

    matched = sorted(jd_tech & resume_tech)
    missing = sorted(jd_tech - resume_tech)

    return {
        "total_jd_keywords": len(jd_tech),
        "matched_keywords": matched,
        "matched_count": len(matched),
        "missing_keywords": missing,
        "missing_count": len(missing)
    }