import React, { useState, useEffect } from 'react';
import List from './components/List';
import tasksService from './services/tasks'


const App = () => {
  const [task, setTask] = useState("")
  const [currentTasks, setCurrentTasks] = useState([]);

  const byId = (o1, o2) => o1.id - o2.id

  useEffect(() => {
    tasksService.getAll()
      .then(initialTasks => {
        setCurrentTasks(initialTasks.sort(byId))
      })
  }, []);

  const handleChange = (event) => {
    setTask(event.target.value)
  }

  const handleToggleComplete = id => {
    const task = currentTasks.find(t => t.id === id)
    const changedTask = { ...task, is_complete: !task.is_complete }

    tasksService
      .update(id, changedTask)
      .then(returnedTask => {
        setCurrentTasks(
          currentTasks.sort(byId).map(
            task => task.id !== id ? task : returnedTask)
        )
      })
  }

  const handleDelete = (id) => {
    tasksService.remove(id).then(() => {
      const updatedTasks = currentTasks.filter(item => item.id !== id)
      setCurrentTasks(updatedTasks)
    })
    .catch(error => console.log(error))
  }

  const handleAdd = async () => {
    const newTask = await tasksService.create({ "task": task })
    const newTasks = currentTasks.concat(newTask)
    setCurrentTasks(newTasks);
    setTask('');
  }

  return (
    <div>
      <h1>Todo list app</h1>
      <List
        list={currentTasks}
        handleToggleComplete={handleToggleComplete}
        handleDelete={handleDelete}
      />
      <div>
        <input type="text" value={task} onChange={handleChange} />
        <button type="button" onClick={handleAdd}>
          Add task
        </button>
      </div>
    </div>
  );
}

export default App;


