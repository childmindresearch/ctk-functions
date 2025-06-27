import enum


class Prompts(enum.StrEnum):
    EXTRACT_DIAGNOSIS = """
In the following clinical report, you will find a section that looks like this:

DSM-5 Diagnoses
309.24/F43.22	Adjustment Disorder, With anxiety
307.51/F50.81	Binge-Eating Disorder

Find this section and extract the codes and names of the diagnoses. Note that it
is possible for there to be no diagnoses, in this case return an empty list.

Diagnoses may come with a classifier. In these cases, include the classifier in the name.

Possible classifiers are as follows:
Confirmed, Presumptive, Requires Confirmation, Rule-out, No Diagnosis, Past, By History

"""

    EXTRACT_PARTICIPANT = """
In the following clinical report, you should look for the participant's first name.
Return only their first name.
"""
    HBN_REPORT_SUMMARY = """The following is a part of a Healthy Brain Network (HBN)
    report summarising developmental and mental
health assessment of a child. It has been written for psychologists and
other mental health professionals. Shorten it and rephrase it to make it
easier to understand for parents that are not mental health professionals
and might come from various backgrounds. Write in the style of a school
textbook. Do not assume any level of education for parents. Provide context
for the provided diagnoses. Do not change the list of diagnoses, do not
alter the names of the diagnoses, but exclude their DSM-5 number. The
response should have the following structure: 1. a short introduction, 2.
list the diagnoses, 3. provide a summary of the report, 4. a closing section
with advice and a thank you. Do not include header names in the letter. Do
not include a greeting like “Dear parents” or a closing like “Sincerely, …”.

The introduction should be, verbatim, as follows:

“We appreciate your time and patience during [FIRST_NAME]'s participation at
the Healthy Brain Network. This letter is a summary of the results of the
assessments. The results are based on the information you provided, the
information [FIRST_NAME] provided, and the results of the assessments. For
more detailed information, please refer to the clinical report.”

The list of diagnoses can take one of two forms

1) If there are no diagnoses to report, the paragraph should start with “Your
child's assessment results did not lead to any diagnoses.” and end there.
2) If there are diagnoses to report, the paragraph should start with “Your
child's assessment results led to the
following diagnoses:”, followed by an empty line and then a numbered list of diagnoses without
their DSM-5 number. Include all classifiers in this list i.e. do not separate
ruled-out diagnoses from confirmed or similar. This list is followed by a new paragraph starting with “To explain
these diagnoses in simple
language” followed by explanations of these diagnoses in simple terms.
The names of the diagnoses should never be altered or simplified.
Only provide an explanation of the diagnoses without specific examples e.g.
do not say something like "These challenges can affect their daily life,
including school and social interactions." Examples of explanations are as
follows:

"Your child’s assessment results led to the following diagnoses:

1.	Attention-Deficit/Hyperactivity Disorder, Predominantly inattentive presentation
2.	Language Disorder (rule-out)

To explain these diagnoses in simple language:

[FIRST_NAME] was diagnosed with Attention-Deficit/Hyperactivity Disorder (ADHD), Predominantly Inattentive presentation. This means that [FIRST_NAME] frequently displays signs of inattention and is often easily distracted. This will need some special attention and strategies to help enhance focus and attention span.

[FIRST_NAME] was also flagged for a potential Language Disorder which means there could be difficulties with the proper use of language for communication. This needs to be explored further in order to assess for this diagnosis."

The summary of the report should go over all the assessments in the report
in a way that is easy to understand for parents. Always include the exact
score (Low Average, Average, etc…) for each tested component as well as
their name, but do not include the percentile. The summary should be no longer
than 600 words. An example score pararaph is as follows:

"When it comes to academics, [FIRST_NAME] did well in both reading and math.
[FIRST_NAME]’s reading skills, including recognizing words and decoding, reading fluently,
and comprehension, were Above Average. In math, [FIRST_NAME] was significantly advanced
in doing calculations, applying problem-solving skills, and keeping a quick pace, scoring Above Average.
[FIRST_NAME]’s spelling was Average."

The closing paragraph should be, verbatim, as follows:

“The evaluation provides helpful insight into [FIRST_NAME]'s strengths and
areas in which support may be needed. Accordingly, it will be beneficial for
[FIRST_NAME] and you to work with qualified professionals to address areas
of concern.

On behalf of the Health Brain Network at the Child Mind Institute, thank you
and [FIRST_NAME] for your patience and commitment to completing this
evaluation. We hope that the results will be helpful.”

Only working memory is assessed, not short or long term memory. The language
abilities tested here should be collectively referred only as “core
language”, not just “language”.

Ensure that the entire test is written in the style of a school textbook and that
the text flows naturally, i.e. do not use inline lists.

Diagnoses will come with a classifier. Descriptions of the classifiers are as follows:

- Confirmed: Full criteria for a diagnosis are met and HBN is assigning the diagnosis to the participant. HBN’s evaluation protocols are sufficient in making the diagnosis. No extra specifier is needed.
- Presumptive: Full criteria are likely met based on our evaluation and history of impairment, though HBN is unable to confirm the diagnosis due to a limitation in our evaluation protocol. The recommendations could be implemented without the need for additional testing.
- Requires Confirmation: Full criteria are likely met based on our evaluation and history of impairment, though HBN is unable to confirm the diagnosis due to a limitation in our evaluation protocol. Additionally, there is less evidence from our evaluation AND historic impairment and so less certainty than Presumptive. The disorder would require further testing in order to confirm the diagnosis. The recommendations could be implemented without the need for additional testing.
- Rule-out: Symptoms of a disorder are not clearly defined within one diagnostic criteria and/or are similar or overlap with other presenting disorders. OR Insufficient information in the HBN evaluation to make a diagnosis (or to say that the child definitively does not have a diagnosis), but concerns or vulnerabilities were evident that should be further evaluated /monitored.
- No Diagnosis: The evaluation was completed and symptoms reported do not meet diagnostic criteria for any disorder.
- Past: Full criteria for a disorder were reported during Mental Health Interview, though symptoms are reported to be no longer present for the past 2 months.
- By History: A diagnosis of a disorder was reported during the HBN evaluation, though HBN is unable to confirm this diagnosis, either because the diagnosis is not fully assessed by HBN OR there was insufficient evidence on the HBN evaluation to confirm the previous diagnosis.

Format your response as Markdown."""
