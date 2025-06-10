import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def add_task(task,priority):
    r.zadd("todo_zset",{task:priority})
    r.xadd("todo-stream",{"action":"add","task":task})
    r.lpush("todo_list", task)

def del_task(task):
    r.zrem("todo_zset",task)
    r.xadd("todo-stream",{"action":"delete","task":task})
    r.lrem("todo_list", 1, task)

def show_tasks():
    return [task for task in r.zrange("todo_zset",0,-1)]

def show_recent_tasks():
     return r.lrange("todo_list", -5, -1)

def edit_task(prev_task,new_task,new_priority):
    r.zrem("todo_zset",prev_task)
    r.lrem("todo_list",1,prev_task)
    r.xadd("todo-stream", {"action": "edit", "prev_task": prev_task, "new_task": new_task})
    r.zadd("todo_zset", {new_task: new_priority})
    r.lpush("todo_list", new_task)
    print("Edited the task successfully")
    

def main():
    while True:
        print("--MENU--")
        print("1.Add a task")
        print("2.delete a task")
        print("3.show all tasks")
        print("4. Show 5 recently added tasks")
        print("5.Quit")
        print("6.Edit a task")
        choice = input("Enter the number based on your choice: ")

        if choice == "1":
            task = input("Enter Task :")
            p = input("Enter its priority on the scale of (1-10): ")
            add_task(task,int(p))
            print("Task added")
            print("\n")

        elif choice=="2":
            task = input("Enter task name to delete")
            del_task(task)
            print("Task deleted")
            print("\n")

        elif choice == "3":
            tasks = show_tasks()
            print("Tasks:")
            for t in tasks:
                print(t)
            print("\n")

        elif choice == "4":
            tasks = show_recent_tasks()
            for t in tasks:
                print(t)
            print("\n")

        elif choice == "5":
            break
        elif choice == "6":
            prev_task = input("Enter the task you want to edit: ")
            new_task = input("Enter the new task name: ")
            new_priority = int(input("Enter the new priority (1 - 10 )"))
            edit_task(prev_task,new_task,new_priority)
            print("\n")
            

        else:
            print("invalid input.Try again")
            print("\n")

if __name__ == "__main__":
    main()
        





