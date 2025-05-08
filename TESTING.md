Test case 1:
python3 tracker.py 60001

python3 airport.py 50001 Jellyopolis 60001 localhost 

python3 passenger_gui.py 50010 60001 localhost

Output:
MacBook-Air-600:pythonProject trishasrikanth$ python3 airport.py 50001 Jellyopolis 60001 localhost 

 [ Airport Peer Initialind : Jellyopolis/50001. Tracker: 60001 ] 

Send register message to tracker.

Received response 30 from tracker. 

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE/Kejjn6VG3BE/tMZ2VABdaJiHe+4XezJ\nTc2odnVMpP5HIXTaPDEAwfxpyP445nLuKxkPdH80pWUmdxSCEDWu5g==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Jellyopolis registered with tracker.

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE/Kejjn6VG3BE/tMZ2VABdaJiHe+4XezJ\nTc2odnVMpP5HIXTaPDEAwfxpyP445nLuKxkPdH80pWUmdxSCEDWu5g==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Adding transaction to mempool: Arrival for Alice Jones

Mining….
Mined in 0.013s @ difficulty 2

Block added to blockchain: 1
Skipping Self

Adding transaction to mempool: Departure for Ava Jones

Mining….
Mined in 0.004s @ difficulty 2

Block added to blockchain: 2
Skipping Self

Test case 2:
python3 tracker.py 60001

python3 airport.py 50001 Jellyopolis 60001 localhost python3 airport.py 50002 Seaville 60001 localhost python3 airport.py 50003 Lovelytown 60001 localhost 

python3 passenger_gui.py 50010 60001 localhost

Output:
MacBook-Air-600:pythonProject trishasrikanth$ python3 airport.py 50001 Jellyopolis 60001 localhost 

 [ Airport Peer Initialind : Jellyopolis/50001. Tracker: 60001 ] 

Send register message to tracker.

Received response 30 from tracker. 

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Jellyopolis registered with tracker.

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
2) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEro6xLwIdVMcer0RlpTLtBfRdqX/5mMd2\n5XeBwRgMeGBWdtiMOGQjL+JduAEu8I/Om0epBEcHDSTCMNzf0esWww==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
2) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEro6xLwIdVMcer0RlpTLtBfRdqX/5mMd2\n5XeBwRgMeGBWdtiMOGQjL+JduAEu8I/Om0epBEcHDSTCMNzf0esWww==\n-----END PUBLIC KEY-----\n'
3) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEdlW3AeQ0yzJHzKS8+t7d7X5C2HvFe0MG\nNRa3YM/g69c7DoaqdY3XFG9Gj14RlRS8cQmyX0KUam3Ek0f/McQlNg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
2) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEro6xLwIdVMcer0RlpTLtBfRdqX/5mMd2\n5XeBwRgMeGBWdtiMOGQjL+JduAEu8I/Om0epBEcHDSTCMNzf0esWww==\n-----END PUBLIC KEY-----\n'
3) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEdlW3AeQ0yzJHzKS8+t7d7X5C2HvFe0MG\nNRa3YM/g69c7DoaqdY3XFG9Gj14RlRS8cQmyX0KUam3Ek0f/McQlNg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Adding transaction to mempool: Arrival for Alice Jones

Mining….
Mined in 0.01s @ difficulty 2

Block added to blockchain: 1
Skipping Self
Proposing to : Seaville
Proposing to : Lovelytown

Adding transaction to mempool: Departure for Bob Jones

Mining….
Mined in 0.005s @ difficulty 2

Block added to blockchain: 2
Skipping Self
Proposing to : Seaville
Proposing to : Lovelytown
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
2) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEro6xLwIdVMcer0RlpTLtBfRdqX/5mMd2\n5XeBwRgMeGBWdtiMOGQjL+JduAEu8I/Om0epBEcHDSTCMNzf0esWww==\n-----END PUBLIC KEY-----\n'
3) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEdlW3AeQ0yzJHzKS8+t7d7X5C2HvFe0MG\nNRa3YM/g69c7DoaqdY3XFG9Gj14RlRS8cQmyX0KUam3Ek0f/McQlNg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Lovelytown
Orphaned block 1 (parent 0        not found)
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEpOhjRlh/kNOTvWsac491Smu9ZWGP4uka\nNNjiflLyNhJGS9WkX7Z0FSQA98/Gq6HUIeE1GFD5zL862PyXd03edQ==\n-----END PUBLIC KEY-----\n'
2) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEro6xLwIdVMcer0RlpTLtBfRdqX/5mMd2\n5XeBwRgMeGBWdtiMOGQjL+JduAEu8I/Om0epBEcHDSTCMNzf0esWww==\n-----END PUBLIC KEY-----\n'
3) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEdlW3AeQ0yzJHzKS8+t7d7X5C2HvFe0MG\nNRa3YM/g69c7DoaqdY3XFG9Gj14RlRS8cQmyX0KUam3Ek0f/McQlNg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Seaville
Orphaned block 1 (parent 0        not found)
Received block proposal from Seaville
Orphaned block 2 (parent 000205bb not found)
Received block proposal from Seaville
Orphaned block 3 (parent 0038b36f not found)

Test case 3:
python3 tracker.py 60001

python3 airport.py 50001 Jellyopolis 60001 localhost python3 airport.py 50002 Seaville 60001 localhost python3 airport.py 50003 Lovelytown 60001 localhost python3 airport.py 50004 Busyham 60001 localhost python3 airport.py 50005 Quaintville 60001 localhost python3 airport.py 50006 Smokeville 60001 localhost

python3 passenger_gui.py 50010 60001 localhost

Output:
MacBook-Air-600:pythonProject trishasrikanth$ python3 airport.py 50006 Smokeville 60001 localhost

 [ Airport Peer Initialind : Smokeville/50006. Tracker: 60001 ] 

Send register message to tracker.

Received response 30 from tracker. 

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Smokeville registered with tracker.

Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Busyham
Orphaned block 1 (parent 0        not found)
Received block proposal from Busyham
Orphaned block 2 (parent 00ff9aea not found)
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Seaville
Orphaned block 1 (parent 0        not found)
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Adding transaction to mempool: Arrival for Avi Curbungen

Mining….
Mined in 0.007s @ difficulty 2

Block added to blockchain: 1
Proposing to : Jellyopolis
Proposing to : Lovelytown
Proposing to : Seaville
Proposing to : Busyham
Proposing to : Quaintville
Skipping Self

Adding transaction to mempool: Departure for Eden Plunkera

Mining….
Mined in 0.016s @ difficulty 2

Block added to blockchain: 2
Proposing to : Jellyopolis
Proposing to : Lovelytown
Proposing to : Seaville
Proposing to : Busyham
Proposing to : Quaintville
Skipping Self
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 

Adding transaction to mempool: Arrival for Olaf Buntingson

Mining….
Mined in 0.004s @ difficulty 2

Block added to blockchain: 3
Proposing to : Jellyopolis
Proposing to : Lovelytown
Proposing to : Seaville
Proposing to : Busyham
Proposing to : Quaintville
Skipping Self
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Quaintville
Orphaned block 1 (parent 0        not found)
Updated Airport Directory
--------------------------------------- 
1) Jellyopolis IP: 127.0.0.1/50001, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBjPgksK/nBzhhj+UxmAYNuzWDOOJNPS8\nRhC4vjRmc/oSEX3Y7fop5cyTmKklERclDYVGOdnvmmjro5yNHeBUnA==\n-----END PUBLIC KEY-----\n'
2) Lovelytown IP: 127.0.0.1/50003, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE3S1WS+EE/2v9EsI9oiOmgSFRwPct8MBp\n6pvjwkRRPk5ml9pNVYHO+i0eboEIHYPsAkT3J3dQHwheEnidX06B2w==\n-----END PUBLIC KEY-----\n'
3) Seaville IP: 127.0.0.1/50002, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEVSHO9UCevxZgtD34Z4SPF22XgHVptonh\nPEBwo8aqtVpRQn/uGVFMsXqHJROxSE5cWu3Ut+BA+YP9GIKCU/gdYA==\n-----END PUBLIC KEY-----\n'
4) Busyham IP: 127.0.0.1/50004, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEfzbPN9J7P8eYpKOa3hy19/qyKPjwheF+\n5APjAGjU1U+/7kAFOT64+wVOejbzMNHBNQLeIIHxov6pBWfTwLllrQ==\n-----END PUBLIC KEY-----\n'
5) Quaintville IP: 127.0.0.1/50005, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEiwn1uDW2HRt+1jBKgUuZBAljWDVdLVra\nI8YzSoRe3VDLBYvGhvOmM0EfhVUYOlS6cHasGXbxPyznHxFxpTTYBQ==\n-----END PUBLIC KEY-----\n'
6) Smokeville IP: 127.0.0.1/50006, Public Key: b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMSHPbnBcav604ItFH9U/GMsaiQITRv3w\nq8i801u6/cQF4I7wdlMTRuKteh6nQcpIVQz/z/Y3ESZXvwP3zmdPHg==\n-----END PUBLIC KEY-----\n'
--------------------------------------- 
Received block proposal from Jellyopolis
Orphaned block 1 (parent 0        not found)
