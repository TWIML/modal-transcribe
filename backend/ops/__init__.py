"""
This directory hosts all the modal application logic - from the infrastructure and job perspective i.e. setting up the image for running jobs, handling the file storage on the backend, and executing the modal jobs and their workloads on the modal platform infrastructure etc.

No other area of the codebase should handle any logic to do with the modal infrastructure, they can call classes or functions set up here to do that - and only the `api` routes should call from here. The `src` directory code is called here but does not call from here.

There will be folders for each functionality type which eventually will host modal class objects to perform all the functionality for that type of object - along with hosting types for the functionality. The root directory will contain files for the infrastructure configuration - storage, image etc.
"""