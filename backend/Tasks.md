# To Do
1. Next steps are to:
    - delete the old transcription stuff, then clean up the classes & printouts
    - write a coalesce segments method so contiguous blocks from same speaker are banded together (they are likely separated due to silence in between speech)
    - add class attributes to the modal operators (for the src functionality handlers, the filepaths etc. to make things clearer)
    - find a way to make the final type object pydantic models proper classes with methods for writing to file and loading from file and attributes for the filepaths etc. (this may be better as a dataclass, see how to manage)
    - turn the storage stuff into a class & set the paths as class attributes & then create methods for getting filepaths, creating filepaths etc. (will simplify imports, writing and loading will be done in the data structure classes themselves or if not best there can be done here as methods, with class attributes for the final object type pydantic models and then methods to ensure what is loaded is of that type etc. with error handling for it and so forth)
    - rehouse things in the appropriate places - move src stuff to src folder, same for api and ops - segregate functionality
    - better logging for debugging and given commentary of flows, try/excepts + error handling and so forth
    - renaming across classes, methods and areas - come up with some conventions for clarity


## Other notes
    - you deleted the poll status code from modal's example, so if you need that and to get an idea of how to run tasks in the bgd via. spawn and check their status etc. then refer to the github