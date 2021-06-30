from django.shortcuts import render
import json
from eth_typing import abi
from web3 import Web3, contract

import time

from rest_framework import status, views, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

public_key = "0x6BA0C6D52831dCc4D21a0D932574748E9512e2aD"
private_key = "7a4dfac01d753f96bc56acf792b4a1f92389e70595f59618fcc75bf6de444b46"

with open('./contract_source.json', 'r') as file:
    data = file.read()
    obj = json.loads(data)

cont_add = obj['contractAddress']
abi = obj['abis']

address = web3.toChecksumAddress(cont_add)

contract = web3.eth.contract(address=address, abi=abi)


class AddCandidateView(views.APIView):
    def post(self, *args, **kwargs):
        name = self.request.data.get('name')

        nonce = web3.eth.getTransactionCount(public_key)
        txn = contract.functions.addCandidate(name).buildTransaction({
            'chainId':5777,
            'nonce':nonce,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        
        event = contract.events.CandidateAdded().processReceipt(txn_receipt)
        arg_id = event[0]['args']['id']
        user_detail = contract.functions.candidates(arg_id).call()

        data = {
            'txn_hash': web3.toHex(txn_hash),
            'transaction_count': web3.eth.get_transaction_count(public_key),
            'candidate_detail':{
                'id':user_detail[0],
                'name':user_detail[1],
                'vote_count':user_detail[2],
                'address':user_detail[3]
            }

        }
        
        return Response(data)



class GetAllCandidates(views.APIView):
    def get(self, request):
        candidateCount = contract.functions.candidateCount().call()
        
        candidates = []
        for i in range(candidateCount):
            candi = contract.functions.candidates(i+1).call()
            candidates.append(candi)
        
        return Response(candidates)



class VoteCandidate(views.APIView):
    def post(self, request, pk):

        nonce = web3.eth.getTransactionCount(public_key)
        txn = contract.functions.vote(pk).buildTransaction({
            'chainId':5777,
            'nonce':nonce,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        event = contract.events.votedEvent().processReceipt(txn_receipt)
        arg_id = event[0]['args']['_candidateId']
        candidate_detail = contract.functions.candidates(arg_id).call()[3]
        
        data ={
            'Vote':'Success',
            'Your_address':public_key,
            'Candidate_address': candidate_detail
        }

        return Response(data)
