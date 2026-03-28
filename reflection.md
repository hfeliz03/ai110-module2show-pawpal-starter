# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The user should be able to add a pet (allowing to have multiple pets) while informing the app fo that pet's data and necessities. The user should be able to see their daily tasks based on their pet's needs. 
- What classes did you include, and what responsibilities did you assign to each?
1. Owner Represents the pet owner.
Attributes
	•	name
	•	daily_time_available
	•	preferences
Methods
	•	update_preferences()
	•	update_time_available()
2. Pet Represents the pet.
Attributes
	•	name
	•	species
	•	age
	•	tasks (list of tasks for the pet)
Methods
	•	add_task()
	•	remove_task()
	•	get_tasks()
3. Task Represents one pet care task like feeding, walking, meds, or grooming.
Attributes
	•	name
	•	duration
	•	priority
	•	category
	•	completed
Methods
	•	mark_completed()
	•	edit_task()

4. Scheduler Creates the daily plan.

Attributes
	•	owner
	•	pet

Methods
	•	generate_plan()
	•	sort_tasks_by_priority()
	•	explain_plan()

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
