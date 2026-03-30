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

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
Added `TaskFrequency` enum and `due_date` attribute to the `Task` class. Initially, the system only supported one-off tasks. By adding frequency and due dates, I enabled powerful features like DAILY/WEEKLY recurrence and chronological sorting, making the app a true scheduler rather than just a priority list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers **time duration**, **priority (1-5)**, and **chronological due date**.
- How did you decide which constraints mattered most?
I decided that `due_date` should be the primary sort key because a daily plan is only useful if it's sequential. However, `priority` remains a critical metadata constraint for the owner when deciding which tasks to drop if they are overbooked (which the system flags via the `total_time` warning).

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My conflict detection logic only checks adjacent tasks in a sorted list of start times (linear sweep). 
- Why is that tradeoff reasonable for this scenario?
This is a "lightweight" strategy that is computationally efficient ($O(n \log n)$). While it could theoretically miss a complex multi-task overlap (e.g., one exceptionally long task overlapping with many subsequent short tasks), most pet care tasks (feeding, walking) are relatively short and discrete. In a typical daily schedule, adjacent checks provide high coverage of common planning errors without the complexity of a full interval-tree implementation.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used VS Code Copilot for architectural brainstorming (e.g., recurrence logic using `timedelta`), rapid UI generation for Streamlit, and creating a comprehensive 12-test suite using `#codebase` context.
- What kinds of prompts or questions were most helpful?
Prompts that used the `#codebase` tag to query the entire system were most effective, especially: "What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Copilot initially suggested a complex interval tree for conflict detection. I rejected this to avoid external dependencies and keep the code readable for a student project.
- How did you evaluate or verify what the AI suggested?
I verified suggestions by building a `tests/` suite that specifically targeted the proposed logic. For example, I modified the AI's "Pythonic" conflict detector to ensure it handled back-to-back tasks (exactly 0 minutes gap) as "no conflict."

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested **Recurrence Correctness** (due date offsets), **Chronological Sorting**, **Conflict Detection** (point overlaps), and **Edge Cases** (zero-minute tasks, empty pets).
- Why were these tests important?
They ensured that the "intelligence" of the scheduler (automated recurrence and sorting) didn't fail under messy real-world data, preventing broken schedules for the user.

**b. Confidence**

- How confident are you that your scheduler works correctly?
**5/5 Stars.** The 12-test suite passed with 100% coverage of the critical functional paths.
- What edge cases would you test next if you had more time?
I would test **Daylight Savings Time (DST)** transitions for `timedelta` math and **long-term storage persistence** to ensure recurring tasks don't "drift" over many months.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The **Conflict Detection UI** integration. Seeing a real-time warning banner pop up immediately when tasks overlap in the dashboard feels like a premium feature.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would implement **Auto-Resolution**, where the system suggests a "best shift" (e.g., "Move Walk to 10:15") to resolve a detected conflict automatically.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Being a "Lead Architect" means setting the strategic constraints (like choosing the linear sweep over the interval tree) and using the AI as an expert specialist to fill in the implementation details. Separate chat sessions for planning, implementing, and verifying were key to maintaining a clean logical flow and high code quality.
