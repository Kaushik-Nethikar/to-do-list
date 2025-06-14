import streamlit as st
from datetime import datetime
import json

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def add_task(task_text, priority="Medium"):
    """Add a new task to the list"""
    new_task = {
        'id': len(st.session_state.tasks),
        'text': task_text,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'priority': priority
    }
    st.session_state.tasks.append(new_task)

def toggle_task(task_id):
    """Toggle task completion status"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

def delete_task(task_id):
    """Delete a task from the list"""
    st.session_state.tasks = [task for task in st.session_state.tasks if task['id'] != task_id]

def clear_completed():
    """Remove all completed tasks"""
    st.session_state.tasks = [task for task in st.session_state.tasks if not task['completed']]

# App title and description
st.title("📋 My To-Do List")
st.markdown("*Stay organized and get things done!*")

# Sidebar for task management
with st.sidebar:
    st.header("➕ Add New Task")
    
    # Task input
    new_task = st.text_input("What needs to be done?", placeholder="Enter your task here...")
    
    # Priority selection
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    
    # Add task button
    if st.button("Add Task", type="primary"):
        if new_task.strip():
            add_task(new_task.strip(), priority)
            st.success("Task added!")
            st.rerun()
        else:
            st.error("Please enter a task!")
    
    st.divider()
    
    # Filter options
    st.header("🔍 Filter Tasks")
    filter_option = st.selectbox("Show:", ["All Tasks", "Active Tasks", "Completed Tasks"])
    
    priority_filter = st.selectbox("Priority Filter:", ["All Priorities", "High", "Medium", "Low"])
    
    st.divider()
    
    # Statistics
    st.header("📊 Statistics")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([task for task in st.session_state.tasks if task['completed']])
    active_tasks = total_tasks - completed_tasks
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", total_tasks)
        st.metric("Active", active_tasks)
    with col2:
        st.metric("Done", completed_tasks)
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            st.metric("Progress", f"{completion_rate:.0f}%")

# Main content area
if not st.session_state.tasks:
    st.info("🎯 No tasks yet! Add your first task using the sidebar.")
else:
    # Filter tasks based on selection
    filtered_tasks = st.session_state.tasks.copy()
    
    if filter_option == "Active Tasks":
        filtered_tasks = [task for task in filtered_tasks if not task['completed']]
    elif filter_option == "Completed Tasks":
        filtered_tasks = [task for task in filtered_tasks if task['completed']]
    
    if priority_filter != "All Priorities":
        filtered_tasks = [task for task in filtered_tasks if task['priority'] == priority_filter]
    
    if not filtered_tasks:
        st.info(f"No tasks found for the selected filter: {filter_option}")
    else:
        # Display tasks
        st.subheader(f"📝 {filter_option}")
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Clear Completed"):
                clear_completed()
                st.rerun()
        with col2:
            if st.button("Clear All"):
                st.session_state.tasks = []
                st.rerun()
        
        st.divider()
        
        # Display each task
        for task in filtered_tasks:
            with st.container():
                col1, col2, col3, col4 = st.columns([0.5, 3, 1, 0.5])
                
                with col1:
                    # Checkbox for completion
                    if st.checkbox("", value=task['completed'], key=f"check_{task['id']}"):
                        if not task['completed']:
                            toggle_task(task['id'])
                            st.rerun()
                    else:
                        if task['completed']:
                            toggle_task(task['id'])
                            st.rerun()
                
                with col2:
                    # Task text with strikethrough if completed
                    if task['completed']:
                        st.markdown(f"~~{task['text']}~~")
                    else:
                        st.markdown(task['text'])
                    
                    # Show creation time and priority
                    priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    st.caption(f"{priority_color[task['priority']]} {task['priority']} • Added: {task['created_at']}")
                
                with col3:
                    # Status badge
                    if task['completed']:
                        st.success("✅ Done")
                    else:
                        st.info("⏳ Active")
                
                with col4:
                    # Delete button
                    if st.button("🗑️", key=f"del_{task['id']}", help="Delete task"):
                        delete_task(task['id'])
                        st.rerun()
                
                st.divider()

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit* 🚀")

# Export/Import functionality (bonus feature)
with st.expander("🔧 Advanced Options"):
    st.subheader("Export/Import Tasks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Tasks"):
            if st.session_state.tasks:
                tasks_json = json.dumps(st.session_state.tasks, indent=2)
                st.download_button(
                    label="Download tasks.json",
                    data=tasks_json,
                    file_name=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No tasks to export!")
    
    with col2:
        uploaded_file = st.file_uploader("📥 Import Tasks", type=['json'])
        if uploaded_file is not None:
            try:
                imported_tasks = json.loads(uploaded_file.read())
                st.session_state.tasks.extend(imported_tasks)
                st.success(f"Imported {len(imported_tasks)} tasks!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing tasks: {str(e)}")