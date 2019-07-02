Background
------

The original application only allowed one resume per user. As such, 
it already had a concept of "Resume Item" (possibly with existing data).

The brief was to add enough functionality to be able to manage multiple 
resumes, in a short amount of time.


Data Modeling
------

Two models were added:

- `Resume` stores resume-specific elements like title, metadata, and intro copy.
- `ResumeItemLink` maps resume items to models, and also allows for 
    relationship-specific metadata, like order in the list.

This model allows for flexibility in future expansion, while being simple enough 
to manage entirely in the Django ORM without custom code or libraries.
Should we encounter scalability challenges, it can be denormalized later with 
minimal disruption.

See `models.png` for details.


UI Modeling
------

See `UI.png` for starting mockup, and other pngs for result. 
Some additional styling would be preferable.


Implementation
------

No tests were present and there was no indication of whether it was acceptable 
to extend app requirements to include a UI-testing framework, so they were omitted.
Should we have the time to go test-first, I would concentrate attention on the 
data-input entry points in ResumeCreate and ResumeEdit; at the moment we mostly 
rely on the generic views to do the right thing, with minimal defensive coding, 
so there is probably space for improvement. Similarly for the pre-existing views.

The built-in Class-based Generic Views were used because they implement most of 
the basic logic required for CRUD operations.

A feature to manage the ordering with a bit of javascript was planned but 
eventually not implemented due to time constraint.

