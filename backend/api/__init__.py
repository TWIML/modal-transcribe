"""
This directory hosts all the api routes and logic for handling http calls - the user via. the frontend will be hitting these endpoints, look in the frontend to see where these routes are called, and look here to know what is expected to be received by each endpoint. Preferably create types herein to maintain consistency of what is expected.

This directory should only call & import code from the `ops` directory in order to submit jobloads to the modal 'workers' - it should never handle modal operations itself such as managing files etc.

Use Bruno on these routes to check the api calls work as expected.
"""