import base64
with open("sample.pdf", "rb") as f:
    print(base64.b64encode(f.read()).decode())