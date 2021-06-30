# election-daap
A Decentralized Ethereum Voting Application. 

## Features
1. Only one candidate can be added from one address
2. Voter can only vote once
3. All the vote casted can openly seen in the blockchain.
3. Each candidate's data is visible to every node on the blockchain.
4. This app solves the problem of double-voting and hacking the EVM.

## Dependicies
### * Install these prerequisites to follow along with the tutorial. See free video tutorial or a full explanation of each prerequisite. 
  - NPM: https://nodejs.org 
  - Truffle: https://github.com/trufflesuite/truffle 
  - Ganache: http://truffleframework.com/ganache/ 
  - Metamask: https://metamask.io/ 
  
### * Clone the project before getting started with installing and usage
### * Installing dependicies 
  - ```
    cd election-daap
    virtualenv env
    env\Scripts\activate
    ```
  - ```
    pip install -r requirements.txt
    ```
### * Start Ganache
  - Open the Ganache GUI client that you downloaded and installed. This will start your local blockchain instance. See any free video tutorial for full explanation.

### * Compile & Deploy Election Smart Contract
  - This will compile the contract and build all the required artifiacts in the build/contracts folder
    ```
    truffle compile
    ```
   
  - This will deploy the smart contract and will save the abi, contract's address in the elections/contract_source.json 
  - NOTE : The contract is meant to be deployed only once in the production env. 
  - You can default account's credentials in the deploy.py, line 11 and 13.
    ```
    python deploy.py
    ```
### * Run the Django Backend Server
  - This will run the django rest server and you can access all the endpoints of the election's contract.
  - For using the endpoints in frontend apps, just fetch the api. Read the Swagger doc at http://127.0.0.1:8000/, after running the local server.
  ```
  cd elections
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```