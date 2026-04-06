## Report: Customer Support Email Drafting Prototype

### Business Use Case  
This project focuses on automating the drafting of customer support email responses. The system is designed for customer support representatives who need to respond to customer inquiries efficiently and consistently. The input consists of a customer message and relevant company policy or context, and the output is a professional, polite, and actionable email reply.  

This task is valuable because many customer support interactions are repetitive and time-sensitive. Automating first-pass drafts can reduce response time, improve consistency, and allow human agents to focus on more complex or sensitive cases.

---

### Model Choice  
I used the Gemini **2.5 Flash** model via the Google Generative AI API. I chose this model because it is fast, cost-effective, and performs well on structured writing tasks such as drafting emails.  

The model generally produced fluent and context-aware responses, but it required careful prompt design to ensure it followed instructions and did not introduce unsupported details.

---

### Baseline vs. Final Design  

**Baseline Prompt:**  
The initial prompt asked the model to generate a professional customer support reply. While outputs were fluent, the model sometimes implied access to information it did not have or failed to handle missing policy details clearly.

**Final Prompt:**  
The prompt was revised to include stricter rules, such as:
- not inventing policies or details  
- explicitly stating uncertainty when information is missing  
- distinguishing between missing customer information and missing policy context  

**Improvements:**  
The revised prompt reduced hallucination and produced more grounded responses, especially in ambiguous cases. Outputs became more consistent in tone and clearer in next steps, while overall helpfulness remained strong.

---

### Limitations and Human Review  
The system still has limitations. It may occasionally imply capabilities it does not actually have or struggle with complex, ambiguous, or emotionally sensitive cases. It also cannot verify real customer data.  

Human review is necessary for edge cases, policy disputes, and important customer interactions to ensure accuracy and appropriateness.

---

### Deployment Recommendation  
I would recommend deploying this system as a drafting assistant rather than a fully automated solution. It should generate first-pass responses that are reviewed by a human before being sent.  

This approach is most effective when tasks are repetitive, policies are clearly provided, and human oversight is available. Under these conditions, the system can improve efficiency while maintaining reliability.
