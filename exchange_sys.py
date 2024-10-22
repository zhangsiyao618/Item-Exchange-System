## 物品交换系统
## 功能：1.添加物品 2.删除物品 3.显示物品 4.查找物品 0.退出
## 作者: [张思瑶]
## 日期: 2024年10月15日

import tkinter as tk   #快速创建GUI应用程序
from tkinter import messagebox  #显示消息或警告）
from tkinter import simpledialog  #对话框

class ItemExchangeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Exchange System")
        self.items = []
        messagebox.showinfo("Welcome", "Welcome to Item Exchange System (｡･ω･｡)")  # 弹出欢迎信息
        self.main_menu() # 主菜单页面

    def main_menu(self):
        # 清空窗口内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 设置主菜单标题
        title_label = tk.Label(self.root, text="Item Exchange System", font=("Arial", 15))
        title_label.pack(pady=10)

        # 设置功能按钮
        add_button = tk.Button(self.root, text="Add Item", width=10, command=self.add_item_page)
        add_button.pack(pady=2)
        delete_button = tk.Button(self.root, text="Delete Item", width=10, command=self.delete_item_page)
        delete_button.pack(pady=2)
        list_button = tk.Button(self.root, text="Item List", width=10, command=self.list_items_page)
        list_button.pack(pady=2)
        search_button = tk.Button(self.root, text="Search Item", width=10, command=self.search_item_page)
        search_button.pack(pady=2)
        empty_space = tk.Label(self.root, text="")
        empty_space.pack(pady=5)

    # 添加物品页面
    def add_item_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # 添加返回主菜单按钮
        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        name_label = tk.Label(self.root, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        desc_label = tk.Label(self.root, text="Description:")
        desc_label.grid(row=2, column=0, padx=10, pady=10)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=10)

        owner_label = tk.Label(self.root, text="Owner Info:")
        owner_label.grid(row=3, column=0, padx=10, pady=10)
        self.owner_entry = tk.Entry(self.root)
        self.owner_entry.grid(row=3, column=1, padx=10, pady=10)

        add_button = tk.Button(self.root, text="Add", command=self.add_item)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)

    def add_item(self):
        name = self.name_entry.get()
        description = self.desc_entry.get()
        owner = self.owner_entry.get()
        if name and description and owner:
            self.items.append({'name': name, 'description': description, 'owner': owner})
            messagebox.showinfo("Success", f"'{name}' has been added!")
            self.clear_entries()
        else:
            messagebox.showerror("Failure", "Please complete the missing information!")

    # 删除物品页面布局
    def delete_item_page(self): 
        for widget in self.root.winfo_children():
            widget.destroy()
        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        del_label = tk.Label(self.root, text="Delete Item:")
        del_label.grid(row=1, column=0, padx=10, pady=10)
        self.del_entry = tk.Entry(self.root)
        self.del_entry.grid(row=1, column=1, padx=10, pady=10)
        del_button = tk.Button(self.root, text="Delete", command=self.remove_item)
        del_button.grid(row=2, column=0, columnspan=2, pady=20)

    def remove_item(self):
        name = self.del_entry.get()
        matching_items = [item for item in self.items if item['name'] == name]

        if matching_items:
            if len(matching_items) == 1:
                # 只有一个匹配的物品，直接删除
                self.items.remove(matching_items[0])
                messagebox.showinfo("Success", f"'{name}' has been deleted!")
            else:
                # 多个同名物品，让用户选择具体的物品
                item_list = "\n".join([f"{index+1}. Name: {item['name']}, Description: {item['description']}, Owner Info: {item['owner']}"
                                       for index, item in enumerate(matching_items)])
                selection = simpledialog.askstring("Choose one", f"Found multiple items named {name}. Please choose the exact item:\n{item_list}\n\nPossible number(s): (1-{len(matching_items)})")

                try:
                    index_to_delete = int(selection) - 1
                    if 0 <= index_to_delete < len(matching_items):
                        self.items.remove(matching_items[index_to_delete])
                        messagebox.showinfo("Success", f"'{matching_items[index_to_delete]['name']}' has been deleted!")
                    else:
                        messagebox.showerror("Failure", "Invalid input.")
                except (ValueError, TypeError):
                    messagebox.showerror("Failure", "Invalid input.")
        else:
            messagebox.showwarning("No result", f"Found no item named '{name}'.")

    # 显示物品列表
    def list_items_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.pack(padx=10, pady=10, anchor='w')

        if not self.items:
            messagebox.showinfo("Item List", "Empty.")
        else:
            item_list = "\n".join([f"{index+1}. Name: {item['name']}, Description: {item['description']}, Owner Info: {item['owner']}"
                                   for index, item in enumerate(self.items)])
            list_label = tk.Label(self.root, text="Item List:", font=("Arial", 14))
            list_label.pack(pady=10)
            items_text = tk.Text(self.root, width=50, height=15)
            items_text.insert(tk.END, item_list)
            items_text.config(state='disabled')  # 禁止编辑
            items_text.pack(padx=10, pady=10)

    # 查找物品页面
    def search_item_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        back_button = tk.Button(self.root, text="Back", command=self.main_menu)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        search_label = tk.Label(self.root, text="Search Item:")
        search_label.grid(row=1, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)

        search_button = tk.Button(self.root, text="Search", command=self.search_item)
        search_button.grid(row=2, column=0, columnspan=2, pady=20)

    def search_item(self):
        name = self.search_entry.get()
        matching_items = [item for item in self.items if item['name'] == name]

        if matching_items:
            item_list = "\n".join([f"{index+1}. Name: {item['name']}, Description: {item['description']}, Owner Info: {item['owner']}"
                                   for index, item in enumerate(matching_items)])
            messagebox.showinfo("Found!", f"{item_list}")
        else:
            messagebox.showwarning("No result", f"There is no item named '{name}'.")

    # 清空所有输入框
    def clear_entries(self):
        if hasattr(self, 'name_entry'):
            self.name_entry.delete(0, tk.END)
        if hasattr(self, 'desc_entry'):
            self.desc_entry.delete(0, tk.END)
        if hasattr(self, 'owner_entry'):
            self.owner_entry.delete(0, tk.END)
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
        if hasattr(self, 'del_entry'):
            self.del_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemExchangeGUI(root)
    root.mainloop()
