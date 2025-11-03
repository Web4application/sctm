git init                # initialize repo
git add my_sctm_code.py # stage file
git commit -m "Add SCTM code"
git branch -M main
git remote add origin https://github.com/web4application/sctm.git
git push -u origin main

echo "sctm_code_here" > sctm_code.py

pip install fastapi uvicorn psycopg2-binary pydantic
npx create-react-app frontend
cd frontend
npm install axios react-d3-tree
