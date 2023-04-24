# Thought Process
- An academic profile ... based of student's school and current sem e.g. JKUAT 3.1
- So we should render 1.1, 1.2, 2.1 and 2.2 transcrpts
- So their profile could be attached to each of these transcrpts?

- Tho we do need to store units too right? 
- Like each course with it's Course Group being used for the model, right?
- If that's the case we have 4 models this far i.e:
  
Student -AcademcProfile =>Transcripts =>Units

- The academic profile:
  - Stores the current average mark and grade and current honours.
  - Also stores the mark this far for each grouping and how complete that grouping is based on student's school
  - Linked to one or many transcripts
- The transcript:
  - Stores the grades for one semetser, the name of the semester, that semesters average mark and grade, perhaps start and end date
  - Has an AcademicProfile Foreign Key
  - Linked to many units
- The course:
  - Stores the name of the course, it's mark, it's grade, it's Model Grouping
  - Has a Transcript Foreign Key

- Storing units:
  - We can create a model called CourseUnits
  - Stores the units for a particular school
  - Stores the name of the course, it's model grouping, school and semester during which it's offered
  - Can be querried to get the transcript units to render on frontend the first time
  - Querried by passing school and current sem on sign up


# Current Features

> - [ ] App Onboarding
> - [ ] Sign Up
> - [ ] Basic Student Model
> - [ ] Academic Profile - POST & GET
> - [ ] Technical Profile - POST & GET
> - [ ] Work Experience Profile - POST & GET
> - [ ] Soft Skills Profile - POST & GET
> - [ ] Specialisation Prediction & Compatibility Score
> - [ ] More Comprehensive Report
> - [ ] Onboarding the Student through Assistance
> - [ ] Sign In
> - [ ] Forgot Password
> - [ ] Landing
> - [ ] News Filtering

# Plausible Features
> - [ ] Career Roadmap
> - [ ] More Specific Career Path Recommendations
> - [ ] Goal Setting
> - [ ] Create CV
> - [ ] Vision Board
> - [ ] Interview Prep