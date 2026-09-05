# Project_5 — Agentic AI Project

## Problem
A single LLM call is a poor fit for any task that needs several distinct skills applied in sequence with quality control. Ask one prompt to "research this topic and write a reviewed report" and it does everything at once, badly: it does not actually gather sources, it cannot run steps in parallel, it has no separate reviewer to catch weak claims, and it cannot pause for a human to steer it. It also has no memory of what it already found and no way to recover when a tool fails partway through.

**The problem to solve:** decompose a real task into cooperating agents, each with a clear role, tools, and memory, and orchestrate them reliably. The system must delegate work, run independent subtasks in parallel, keep shared state as it goes, loop when quality is not met, pause for human approval, and survive a failed tool call without crashing the whole run.

This forces the student to confront what makes agentic systems hard: role design, communication, state, routing, loops, persistence, and reliability, rather than just calling a model in a chain.