# belay

# Run Instruction
## 1 create conda environment for python
### 1.1 create a conda environment with python 3.11.2
```
conda create -n belay python=3.11.2
```
### 1.2 activate the environment
```
conda activate belay
```
### 1.3 install the requirements
```
python -m pip install -r requirements.txt
```
### 1.4 install flask-cors version 3.0.10
```
python -m pip install flask-cors==3.0.10
```
## 2 Install Node.js version 18.16.0 LTS
https://nodejs.org/
## 3 Start the backend server
```
cd backend
flask run --reload --port=5001
```
## 4 Start the frontend server
```
cd belay
npm run dev
```
## 5 Access Belay at the frontend server URL as shown in the terminal
Have fun!

# Start a `vue.js` project
## 1 install `node.js` version 18.16.0 LTS
https://nodejs.org/
## 2 start a `vue.js` project with `vue.js` version 3.3.2
```
npm init vue@3.3.2

Project name: belay
Add TypeScript? No
Add JSX Support? No
Add Vue Router for Single Page Application Development? Yes
Add Pinia for state management? No
Add Vitest for unit testing? No
Add Cypass for both Unit and End-to-End Testing? No
Add ESLint for code quality? No

cd belay
npm install
```
## 3 install `axios` version 1.3.6
```
npm install axios@1.3.6 --save
```
## 4 install Bootstrap version 5.2.3
```
npm install bootstrap@5.2.3 --save
```

# Attribution
- `vue.js` + flask SPA development: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/