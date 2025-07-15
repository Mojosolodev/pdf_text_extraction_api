import base64
with open("sample.pdf", "rb") as pdf_file:
    base64_string = base64.b64encode(pdf_file.read()).decode("utf-8")
with open("request.json", "w") as f:
    f.write('{"pdf_base64": "' + base64_string + '", "skills": ["Python", "JavaScript", "React"]}')