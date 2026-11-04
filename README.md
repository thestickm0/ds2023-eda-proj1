This is a group project with multiple deliverables spread across the second half of the semester.

You will build an interactive dashboard exploring a dataset of your own choosing, then distill your main finding into a standalone infographic.

Your group may use any data for this project, as long as it is it meets these criteria:

It is tidy or can be converted into tidy form.
It has at least 3 grouping columns and 3 measurement columns.
It has at least 500 observations.
It is not a built-in dataset, such as one available in a package like Seaborn.
If you have questions about datasets, please ask the instructor.

Deliverables
There are multiple deliverables for this project, each with its own submission pages on Canvas.

Please review each deliverables page for instructions and the rubric.

1. Project Proposal
A short written proposal describing your dataset, your motivating research questions, and your planned approach.

2. Dashboard Mockups
Low-fidelity mockups of your planned dashboard, workshopped in class for peer and instructor feedback before implementation.

3. Final Presentations
Each group presents in a 10-minute slot during the last full week of class (after Thanksgiving week).

Two things are presented together in this slot:

Implemented dashboard. Your dashboard should contain at least two sections: an about section and an interactive section.
The about section provides an overview of the dataset and project goals, and highlights a few insights about the data through static visualizations. Think of this like a brief introductory article that catches the audience's attention and gives a sense of what the project is about and its key takeaways.
The interactive section contains at least three charts that meaningfully answer your research questions. Charts can be separate or connected from an interaction standpoint, but each should involve some interactivity, such as widgets (e.g., dropdowns, filters) in addition to micro-interactions (e.g., hovering, zooming). Think carefully about which charts benefit from interactivity and whether it brings real value for a given visualization.
Infographic (draft). A near-final draft of your infographic (see below), presented alongside the dashboard. Feedback from this presentation should inform your revisions before final submission.
Slides from your presentation should be included in your final submission.

4. Final Submission
Select the single main takeaway from your dashboard analysis and design a standalone infographic communicating it, combining text and chart(s) to tell that story clearly to someone who won't interact with the data themselves. You may use one chart or several, depending on what best supports the takeaway; the choice is yours.

This is the version of the infographic you present at final presentations, revised based on the feedback you received there.

Grading
Each deliverable has its own grading rubric, which will be provided separately closer to the relevant due date.


Submission Details
This is a group project.

# RESEARCH QUESTIONS (1 High → 2 Mid-level → Action + Target Each)
**(1) How has the movie industry’s output and commercial performance changed over time?**

*Mid-level 1) How have the number of releases and the average revenue per film changed by year?*

Action: Compute Derived Value then Correlate

Target: count of films and mean revenue per release year, compared against year

*Mid level 2) Which years or decades had unusually high or low total box-office revenue?*

Action: Find Extremes or Anomalies

Target: total revenue aggregated by year or decade.

**(2) How does a movie’s runtime correlate w/ viewership and score?**

*Mid level 1) Do longer runtimes correlate with lower viewership?*

Action: Correlate, Co-Variance, Trend

Target: Plot runtime against ‘popularity’ value and ‘revenue’, see how those change as runtime increases

*Mid level 2) Do longer runtimes correlate with higher scores?*

Action: Correlate, Characterize Distribution

Target: average scores grouped by runtime

**(3) How do genres differ in profitability and audience reception?**

*Mid level 1) How are average ratings spread within each genre, and which genres vary most?*

Action: Characterize Distribution.

Target: vote average, grouped by genre

*Mid level 2) Which genres earn the most median profit, and has that ranking shifted across decades?*

Action: Compute Derived Value, Sort

Target: median profit per genre, per decade

**4. What factors are associated with a movie’s critical success, and is critical success tied to commercial success?**

*Mid level 1) Which genres, runtimes, and directors tend to get the highest audience ratings?*

Action: filter, correlate

Target: vote_average against revenue_adj, grouped by decade (release_year)

*Mid level 2) Do highly rated movies also make more money, and has that relationship changed over time?*

Action: Find anomalies

Target: movies that fall far from the trend between vote_average and revenue_adj
