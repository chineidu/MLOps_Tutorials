# Introduction to Data Structures and Algorithms (DSA)

## Table of Contents
<!-- TOC -->

- [Introduction to Data Structures and Algorithms DSA](#introduction-to-data-structures-and-algorithms-dsa)
  - [Table of Contents](#table-of-contents)
  - [Big O Notation](#big-o-notation)
    - [Time Complexity](#time-complexity)
    - [Space Complexity](#space-complexity)
    - [Complexity Chart](#complexity-chart)
  - [Framework For Solving DSA Problems](#framework-for-solving-dsa-problems)
  - [Important Topics to Cover](#important-topics-to-cover)

<!-- /TOC -->
## Big O Notation

- Big O notation is a mathematical representation used to describe the performance or complexity of an algorithm.

- It describes an algorithm according to how fast it runs (time complexity) or how much memory it uses (space complexity) as the input size grows.

- The time is NOT the actual time taken (seconds, milliseconds, etc.) but rather how the time grows relative to the input size.

- It considers the worst-case scenario, which helps in understanding the upper limits of an algorithm's performance.

### Time Complexity

- This describes the amount of time an algorithm takes to complete as a function of the length of the input.
- Common time complexities include:
  - O(1): Constant time (No change with input size)
  - O(log n): Logarithmic time (Increases slowly as input size increases)
  - O(n): Linear time (Increases linearly with input size)
  - O(n log n): Linearithmic time (Increases slightly more than linearly)
  - O(n^2): Quadratic time (Increases quadratically with input size. e.g. nested loops)
  - O(n^k): Polynomial time (Increases polynomially with input size. e.g. k nested loop. k is a constant)
  - O(2^n): Exponential time (Increases exponentially with input size)
  - O(n!): Factorial time

### Space Complexity

- This describes the amount of memory an algorithm uses as a function of the length of the input.
- Common space complexities include:
  - O(1): Constant space
  - O(n): Linear space
  - O(n^2): Quadratic space
  - O(log n): Logarithmic space
  - etc.

### Complexity Chart

[![image.png](https://i.postimg.cc/vmBhBgGZ/image.png)](https://postimg.cc/RWkKp03k)

## Framework For Solving DSA Problems

1. **Understand the Problem**: Read the problem statement carefully (at least twice). Identify the input, output, and constraints. Clarify any doubts you have about the problem.

2. **Plan Your Approach**: Think about different ways to solve the problem. Start with a brute-force solution if necessary, then look for optimizations. Consider the time and space complexity of your approach.

3. **Write Pseudocode**: Outline your solution in pseudocode. This helps you organize your thoughts and ensures you have a clear plan before you start coding. Use diagrams if they help you visualize the problem.

4. **Implement the Solution**: Write the actual code based on your pseudocode. Focus on correctness first, then optimize if needed. Use meaningful variable names and add comments to explain complex parts of your code.

5. **Optimize and Refine**: Review your code for any potential optimizations. Check if there are any redundant calculations or if you can use more efficient data structures. Ensure your code adheres to best practices.

6. **Check Other Solutions**: After solving the problem, look at other people's solutions. This can provide new insights and techniques that you can learn from.

7. **Practice Regularly**: Practice solving different types of problems regularly. Repeat previously solved problems to reinforce your understanding and improve your problem-solving skills.

## Important Topics to Cover

- Arrays and Hashing
- Two Pointers
- Stacks and Queues
- Binary Search
- Sliding Window
- Linked List
- Trees
