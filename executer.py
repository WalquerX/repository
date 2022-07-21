#!/usr/bin/env python3

import json
import subprocess
import os

# Account id
account_id = "testaccount17.testnet"
store_account = "test051.mintspace2.testnet"

#Assign the filename
filename_events = "db/events.txt"
filename_json = "db/data.json"

def send_nft(receiver, nft):
    #bashCommand = "near call test051.mintspace2.testnet nft_transfer '{\"receiver_id\": \"testaccount17.testnet\",\"token_id\": \"1\"}' --account-id testaccount17.testnet --depositYocto 1"
    process = subprocess.run(["near", "call", store_account, "nft_transfer", '{\"receiver_id\": \"' + receiver + '\",\"token_id\": \"' + nft + '\"}', "--account-id", account_id, "--depositYocto", "1"], capture_output=True)
    #output, error = process.communicate()
    print(process)

# Process only if events.txt has at least one line
with open(filename_events) as file:
    lines = file.readlines()

if lines != []:
    #Get last line of events.txt
    with open(filename_events) as file:
        for line in file:
            pass
        last_line = line

    #Convert it to json object
    data_event = json.loads(last_line)

    # Cargar los NFTs que estoy vigilando para compra y quema.

    with open(filename_json) as f:
        data_nfts = json.load(f)

    # definition of functions

    # NFT transfer
    def check_for_nft_transfer(nft):

        for event in data_nfts:
            for nft_group in event['tickets']:
                if nft_group['nftId'] == nft:
                    
                    send_nft(data_event['data'][0]['new_owner_id'], nft_group['letIn'])
                    
                    print(f"envía $()", nft_group['letIn'])
                    
    # NFT burn
    def check_for_nft_burn(nft):
        
        for event in data_nfts:
            for nft_group in event['tickets']:
                if nft_group['letIn'] == nft:
                    for consumable in nft_group['consumables']:
                        
                        send_nft(data_event['data'][0]['owner_id'], consumable)
                        
                        print(f"envía $()", consumable)
                        
    # funcion principal

    if data_event['event'] == 'nft_transfer':
        check_for_nft_transfer(data_event['data'][0]['token_ids'][0])
    elif data_event['event'] == 'nft_burn':
        check_for_nft_burn(data_event['data'][0]['token_ids'][0])


    # Delete last line of file events.txt
    with open(filename_events, "r+", encoding = "utf-8") as file:

        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > -1:
            file.seek(pos, os.SEEK_SET)
            file.truncate()

else:
    print("No hay eventos para procesar")




    
