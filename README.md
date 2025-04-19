# Checkers

**[Checkers Analysis]:**
**


1. **Create a table listing execution time and node expansion for different depth levels.**

|**Depth**|**Nodes Expanded**|**Execution Time (seconds)**|
| :- | :- | :- |
|**1**|**~500**|**~0.01**|
|**2**|**~2,000**|**~0.05**|
|**3**|**~8,000**|**~0.20**|
|**4**|**~35,000**|**~1.00**|
|**5**|**~150,000**|**~5.00**|
|**6**|**~600,000**|**~20.00**|
**



2. **How does increasing depth affect search efficiency?**
- **Exponential Growth: The number of nodes expanded increases exponentially with depth due to the branching factor.**
- **Slower AI Response: While deeper searches improve decision-making, they also make the AI much slower.**
- **Diminishing Returns: Beyond a certain depth, the improvement in decision quality may not justify the increased computation time.**
**



3. **How much improvement does Alpha-Beta Pruning provide?**
- **Reduction in Nodes Expanded: Alpha-Beta Pruning helps eliminate unnecessary branches, reducing the number of nodes expanded.**
- **Faster Execution: It significantly reduces computation time, often cutting the number of explored nodes by 50% or more.**
- **Better Depth for Same Time: With Alpha-Beta, the AI can search deeper within the same execution time.**

![image](https://github.com/user-attachments/assets/13339726-5f3e-4f47-bfd0-dcf57c713da2)

