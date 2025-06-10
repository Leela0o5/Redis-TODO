import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def add_task(task,priority):
    r.zadd("todo_zset",{task:priority})
    r.xadd("todo-stream",{"action":"add","task":task})

def del_task(task):
    r.zrem("todo_zset",task)
    r.xadd("todo-stream",{"action":"delete","task":task})

def show_tasks():
    return [task for task in r.zrange("todo_zset",0,-1)]

def show_recent_tasks():
    return [t for t in r.zrevrange("todo_zset", 0, 4)]

def main():
    while True:
        print("--MENU--")
        print("1.Add a task")
        print("2.delete a task")
        print("3.show all tasks")
        print("4. Show 5 recently added tasks")
        print("5.Quit")
        choice = input("Enter the number based on your choice: ")

        if choice == "1":
            task = input("Enter Task :")
            p = input("Enter its priority on the scale of (1-10): ")
            add_task(task,p)
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

        else:
            print("invalid input.Try again")
            print("\n")

if __name__ == "__main__":
    main()
        





