#TO DO LIST FULL CODE
import uuid

def main_menu():
    
    global choice
    
    print("""
    == TODO LIST ==
    [1] show task
    [2] add task
    [3] complete task
    [4] exit
    """)
        
    choice = str(input("Your choice: "))


class todo_list():
    
    def add_task(self):
        self.temp_str = []
        
        self.idd = str(uuid.uuid4())
        self.temp_str.append(self.idd)
        
        self.task = input("What is your task? ")
        self.temp_str.append(self.task)
        
        self.deadline = input("What is the deadline? ")
        self.temp_str.append(self.deadline)
    
        try:
            stream = open('todo_list.txt', 'a')
            for i in range(len(self.temp_str)):
                if i != 2:
                    stream.write(self.temp_str[i])
                    stream.write(" | ")
                else:
                    stream.write(self.temp_str[i])
                    stream.write("\n")
            stream.close()
        except Exception as e:
            print('An error occurred:', e)
            
    def show_task(self):
        try:
            stream = open('todo_list.txt', 'r')
            lines = stream.readlines()
            if lines != []:
                for line in lines:
                    print(line, end='')
                stream.close()
            else:
                print('Empty list')
        except Exception as e:
            print('An error occurred:', e)
            
    def remove_task(self):
        self.temp_list2 = []
        self.remove = input("Enter ID to complete: ")
        
        try:
            stream = open('todo_list.txt', 'r')
            lines = stream.readlines()
        
            for line in lines:
                if self.remove not in line:
                    self.temp_list2.append(line)
            
            stream = open('todo_list.txt', 'w')
            for i in self.temp_list2:
                stream.write(i)
            stream.close()
        except Exception as e:
            print('An error occurred:', e)
        
        
user1_list = todo_list()
choice = 0

while choice != '4':
    main_menu()
    if choice == '1':
        user1_list.show_task()
    elif choice == '2':
        user1_list.add_task()
    elif choice == '3':
        user1_list.remove_task()
    elif choice == '4':
        print('Goodbye!')
        break
    else:
        print("Invalid choice. Please try again!")