# Scheduler

## Aims

This script runs a scheduling program, specifically designed to implement a schedule over a 1-year basis (52 weeks), ensuring participants get an equal turn in the schedule. It varies the time length (52 weeks) to ensure all participants have an equal number of turns. 

## Features

The schedule allows users to insert individual unavailable dates. It also ensures that the same person cannot do two weeks in a row. Currently the design is for the schedule to operate on a weekly basis. It also implements a feature to ensure that the pairings of the participants are spaced out so that the same two people do not get paired with each other an excessive amount. 

Finally, the scheduler has an 'update' feature, whereby the user points the program at the current schedule, the scheduler then saves the 'current state' of that schedule and re-forms the rest of the schedule in-line with the unavaliable dates. This is ideal for changes in avaliability of participants part way through a schedule iteration (within the 52-week cycle). 

## Known Issues and Assumptions

The main assumption that this program runs under is that we have an even number of participants and that they have 2-people per week in the schedule. The author encourages edits to overcome this solution, however, one must ensure that the number of times each participant appears in the final schedule is the same. 

