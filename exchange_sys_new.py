"""
物品复活软件
作者: [张思瑶]
日期: 2024年12月10日
该程序旨在帮助大学生管理和交换不再需要的物品，用户可以发布自己不再需要的物品，其他用户可以选择感兴趣的物品进行交换，达到物品“复活”的目的，避免浪费并实现资源共享。
通过图形界面（Tkinter）提供用户交互界面，管理员和普通用户通过不同权限实现各自的功能。所有的物品信息会被保存到本地文件中，以便长期管理和查询。主要功能包括：
1. 物品信息管理：物品具有公共信息，且可以分为不同的类型，不同类型的物品可以有不同的属性，实现物品的高效管理。
2. 管理员功能：管理员可以定义新的物品类型或修改已定义的物品类型，也可以查看所有物品的详细信息，进行删除或修改，这保证了系统的安全与可维护性。
3. 普通用户功能：普通用户需填写基本信息进行注册，经管理员批准后成为正式用户；可以填写信息添加“可复活”物品或根据物品类型和关键字来查询物品（支持部分/模糊匹配）。 
"""
import tkinter as tk
from tkinter import messagebox
from fuzzywuzzy import fuzz
import pickle
from PIL import Image, ImageTk

class ExchangeSystemApp:
    def __init__(self, root):
        '''
        初始化函数
        '''
        self.window = root
        self.window.title('欢迎登录')
        self.window.geometry('450x300')

        # 加载物品信息数据
        self.item_info_file = "item_info.pickle"
        self.load_item_info()

        # 画布
        self.canvas = tk.Canvas(self.window, height=300, width=200)
        self.im = Image.open("image.jpeg")
        new_width = 150
        new_height = 120
        self.im_resized = self.im.resize((new_width, new_height), Image.LANCZOS)
        self.image_file = ImageTk.PhotoImage(self.im_resized)
        self.image = self.canvas.create_image(50, 1, anchor='nw', image=self.image_file)
        self.canvas.pack(side='top')

        # 用户名、密码输入框
        self.var_usr_name = tk.StringVar()
        self.var_usr_pwd = tk.StringVar()
        tk.Label(self.window, text='Username').place(x=80, y=150)
        tk.Label(self.window, text='Password').place(x=80, y=190)
        self.entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=160, y=150)
        self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=190)

        # 登录和注册按钮
        self.btn_login = tk.Button(self.window, text='Log in', command=self.usr_login)
        self.btn_login.place(x=150, y=230)
        self.btn_sign_up = tk.Button(self.window, text='Sign up', command=self.usr_sign_up)
        self.btn_sign_up.place(x=250, y=230)

    def load_user_data(self):
        '''
        加载用户数据，如果文件不存在则创建一个新文件，并设置一个默认的管理员账户。
        '''
        try:
            with open('usrs_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            usrs_info = {'admin': {'password': '123456', 'status': 'approved', 'address': 'SJTU', 'contact': 'zhangsiyao618@163.com'}}
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(usrs_info, usr_file)
        return usrs_info
    
    def load_item_types(self):
        '''
        加载物品类型数据，如果文件不存在则创建一个新文件，并设置默认的物品类型。
        '''
        try:
            with open('item_types.pickle', 'rb') as file:
                item_types = pickle.load(file)
        except FileNotFoundError:
            item_types = {'书籍': {'properties': ['作者','出版社']}, '食品': {'properties': ['生产日期','保质期']}, '工具': {'properties': ['品牌','型号']}}
            with open('item_types.pickle', 'wb') as file:
                pickle.dump(item_types, file)
        return item_types

    def save_item_types(self, item_types):
        '''
        保存物品类型数据到文件。
        参数：
        item_types (dict): 物品类型数据
        '''
        with open('item_types.pickle', 'wb') as file:
            pickle.dump(item_types, file)

    def load_item_info(self):
        '''
        加载物品信息数据，如果文件不存在则返回空字典。
        返回：
        item_info_data(list): 物品信息数据
        '''
        try:
            with open(self.item_info_file, "rb") as f:
                self.item_info_data = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.item_info_data = []  # 如果没有数据文件，初始化为空列表
        return self.item_info_data

    def save_item_info(self):
        '''
        保存物品信息到文件。
        '''
        with open(self.item_info_file, 'wb') as f:
            pickle.dump(self.item_info_data, f)

    def usr_login(self):
        '''
        用户登录页面：
        如果用户存在且密码正确则登录，否则提示错误信息；若用户不存在则提示注册；若用户未审核通过则提示联系管理员。
        '''
        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
        usrs_info = self.load_user_data()

        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]['password']:
                status = usrs_info[usr_name]['status']
                if status == 'approved':
                    self.window.withdraw()  # 隐藏登录窗口
                    if usr_name == 'admin':
                        self.admin_panel()
                    else:
                        self.user_panel(usr_name)
                else:
                    tk.messagebox.showinfo(message='错误提示：用户未审核通过，请联系管理员')
            else:
                tk.messagebox.showinfo(message='错误提示：密码不对，请重试')
        else:
            is_sign_up = tk.messagebox.askyesno('提示', '你还没有注册，请先注册')
            if is_sign_up:
                self.usr_sign_up()

    def usr_sign_up(self):
        '''
        用户注册页面：
        用户填写用户名、密码、地址、联系方式等信息，点击注册后将信息保存到文件中。
        '''
        def sign_to_Mofan_Python():
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            na = new_address.get()
            nc = new_contact.get()

            usrs_info = self.load_user_data()
            if np != npf:
                tk.messagebox.showerror('错误提示', '密码和确认密码必须一样')
            elif nn in usrs_info:
                tk.messagebox.showerror('错误提示', '用户名已存在！')
            else:
                usrs_info[nn] = {'password': np, 'status': 'pending', 'address': na, 'contact': nc}
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(usrs_info, usr_file)
                tk.messagebox.showinfo('欢迎', '你已经成功注册，等待管理员审核')
                window_sign_up.destroy()

        def cancel_sign_up():
            window_sign_up.destroy()

        window_sign_up = tk.Toplevel(self.window)
        window_sign_up.title('Welcome~')
        window_sign_up.geometry('360x250')

        new_name = tk.StringVar()
        tk.Label(window_sign_up, text='User Name').place(x=50, y=10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
        entry_new_name.place(x=130, y=10)

        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='Password').place(x=60, y=50)
        entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
        entry_usr_pwd.place(x=130, y=50)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='Confirm password').place(x=10, y=90)
        entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
        entry_usr_pwd_confirm.place(x=130, y=90)

        new_address = tk.StringVar()
        tk.Label(window_sign_up, text='Address').place(x=70, y=130)
        entry_usr_address = tk.Entry(window_sign_up, textvariable=new_address)
        entry_usr_address.place(x=130, y=130)

        new_contact = tk.StringVar()
        tk.Label(window_sign_up, text='Contact').place(x=70, y=170)
        entry_usr_contact = tk.Entry(window_sign_up, textvariable=new_contact)
        entry_usr_contact.place(x=130, y=170)

        btn_confirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Mofan_Python)
        btn_confirm_sign_up.place(x=120, y=210)

        btn_cancel_sign_up = tk.Button(window_sign_up, text='Cancel', command=cancel_sign_up)
        btn_cancel_sign_up.place(x=200, y=210)


    def admin_panel(self):
        '''
        管理员面板：管理员可以查看待审核用户列表、审核用户、查看用户信息、查看物品列表、修改物品信息、删除物品、查看物品类型、添加物品类型、修改物品类型。
        '''
        admin_window = tk.Toplevel(self.window)
        admin_window.title('管理员面板')
        admin_window.geometry('600x580')

        def update_user_list():
            '''
            更新待审核用户的列表，将状态为 'pending' 的用户显示到列表框中。
            '''
            self.user_listbox.delete(0, tk.END)  # 清空列表框
            usrs_info = self.load_user_data()
            # 筛选出状态为 'pending' 的用户
            pending_users = [user for user, info in usrs_info.items() if info['status'] == 'pending']
            # 将待审核用户显示到列表框中
            for user in pending_users:
                self.user_listbox.insert(tk.END, user)

        def approve_user():
            '''
            批准新用户注册成功，将用户状态改为 'approved'，并保存到文件中。
            '''
            selected_user = self.user_listbox.get(tk.ACTIVE)  # 获取选中的用户
            usrs_info = self.load_user_data()

            if selected_user in usrs_info:
                usrs_info[selected_user]['status'] = 'approved'
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(usrs_info, usr_file)
                tk.messagebox.showinfo(message=f'{selected_user} 已审核通过')
                update_user_list()  # 更新用户列表
            else:
                tk.messagebox.showinfo(message='用户不存在')

        def reject_user():
            '''
            拒绝新用户注册，将用户状态改为 'rejected'，并保存到文件中。
            '''
            selected_user = self.user_listbox.get(tk.ACTIVE)  
            usrs_info = self.load_user_data()

            if selected_user in usrs_info:
                usrs_info[selected_user]['status'] = 'rejected'
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(usrs_info, usr_file)
                tk.messagebox.showinfo(message=f'{selected_user} 已拒绝')
                update_user_list() 
            else:
                tk.messagebox.showinfo(message='用户不存在')

        def view_user_info():
            '''
            查看用户信息，显示用户的地址、联系方式等信息。
            '''
            selected_user = self.user_listbox.get(tk.ACTIVE)  # 获取选中的用户
            usrs_info = self.load_user_data()

            if selected_user in usrs_info:
                user_info = usrs_info[selected_user]
                info_text = f"用户名: {selected_user}\n" \
                            f"地址: {user_info['address']}\n" \
                            f"联系方式: {user_info['contact']}\n" \
                            f"状态: {user_info['status']}"
                tk.messagebox.showinfo(message=info_text)
            else:
                tk.messagebox.showinfo(message='用户不存在')  

        def display_user_list():
            '''
            显示所有用户列表，点击用户名称时可以查看用户信息。
            '''
            top = tk.Toplevel(admin_window)
            top.title("选择用户")
            user_listbox = tk.Listbox(top, height=10, width=40)
            user_listbox.pack(pady=20)
            users_info = self.load_user_data()
            for user in users_info.keys():
                user_listbox.insert(tk.END, user)

            def on_user_select(event):
                '''
                定义Listbox项被选择时的处理函数
                参数：
                event (tk.Event): 事件对象
                '''
                selected_user = user_listbox.get(tk.ACTIVE)  # 获取选中的用户
                usrs_info = self.load_user_data()
                user_info = usrs_info[selected_user]
                info_text = f"用户名: {selected_user}\n" \
                            f"地址: {user_info['address']}\n" \
                            f"联系方式: {user_info['contact']}\n" \
                            f"状态: {user_info['status']}"
                tk.messagebox.showinfo(message=info_text)

            # 绑定选中事件，点击Listbox中的一个用户名时会触发view_user_info
            user_listbox.bind("<Double-1>", on_user_select)

        def add_item_type():
            '''
            添加物品类型，输入物品类型名称和属性，点击保存后将新类型保存到文件中。
            '''
            property_vars = [] 
            def save_new_type():
                name = new_type_name.get()
                properties = [property_var.get() for property_var in property_vars if property_var.get().strip() != ""] 
                if name:
                    item_types = self.load_item_types()
                    item_types[name] = {'properties': properties}
                    self.save_item_types(item_types)
                    tk.messagebox.showinfo("成功", f"物品类型 '{name}' 添加成功！")
                    new_type_window.destroy()
                    update_item_types()
                else:
                    tk.messagebox.showerror("错误", "请输入物品类型名称")

            def add_property_input():
                '''动态添加一个新的属性输入框'''
                property_var = tk.StringVar()
                property_input = tk.Entry(new_type_window, textvariable=property_var)
                property_input.pack(pady=5)
                property_vars.append(property_var)

            new_type_window = tk.Toplevel(admin_window)
            new_type_window.title("添加物品类型")
            new_type_window.geometry("200x350")

            tk.Label(new_type_window, text="物品类型名称:").pack(pady=5)
            new_type_name = tk.StringVar()
            entry_type_name = tk.Entry(new_type_window, textvariable=new_type_name)
            entry_type_name.pack(pady=5)
            property_vars = []

            # 初始添加一个属性输入框
            tk.Label(new_type_window, text="属性:").pack(pady=5)
            add_property_input()
            btn_add_property = tk.Button(new_type_window, text="添加其他属性", command=add_property_input)
            btn_add_property.pack(pady=5)
            btn_save_type = tk.Button(new_type_window, text="保存", command=save_new_type)
            btn_save_type.pack(pady=5)

        def update_items_with_new_properties(item_type_name, modified_properties):
            '''
            更新属于指定物品类型的所有物品，使其属性与新的物品类型属性同步。
            参数:
            item_type_name (str): 被修改的物品类型的名称。
            modified_properties (list): 物品类型的新属性结构。
            '''
            new_properties = {}
            for index, item in enumerate(self.item_info_data):
                if item['type'] == item_type_name:
                    old_properties = item['properties']
                    for prop_name in modified_properties:
                        if prop_name not in old_properties.keys():
                            # 如果新属性在旧属性中不存在，添加新属性，并为其设置默认值（这里默认值可根据业务逻辑调整）
                            new_properties[prop_name] = "未知"
                        else:
                            new_properties[prop_name] = old_properties[prop_name]
                    self.item_info_data[index]['properties'] = new_properties
            self.save_item_info()

        def modify_item_type():
            '''
            修改物品类型，选择一个物品类型后可以修改名称和属性，点击保存后将修改保存到文件中。
            '''
            property_vars = []  # 属性输入框变量列表
            def save_modified_type():
                '''
                保存修改后的物品类型，将原类型删除并添加新类型。
                '''
                selected_type = listbox_item_types.get(tk.ACTIVE)
                modified_properties = []
                if selected_type:
                    new_name = new_type_name.get()
                    modified_properties = [prop_var.get().strip() for prop_var in property_vars]
                    modified_properties = [prop for prop in modified_properties if prop]  # 移除空属性
                    if new_name and modified_properties:
                        # 更新物品类型的名称和属性
                        item_types = self.load_item_types()
                        item_types[new_name] = {'properties': modified_properties}
                        
                        # 删除原来的物品类型
                        if selected_type != new_name:
                            del item_types[selected_type]
                        
                        self.save_item_types(item_types)
                        tk.messagebox.showinfo("成功", f"物品类型 '{selected_type}' 修改为 '{new_name}'")
                        modify_window.destroy()
                    else:
                        tk.messagebox.showerror("错误", "请输入新的物品类型名称和属性")
                else:
                    tk.messagebox.showerror("错误", "请选择要修改的物品类型")

                update_items_with_new_properties(selected_type, modified_properties)

            modify_window = tk.Toplevel(admin_window)
            modify_window.title("修改物品类型")
            modify_window.geometry("300x600")

            # 显示所有物品类型
            item_types = list(self.load_item_types().keys())
            listbox_item_types = tk.Listbox(modify_window)
            for item in item_types:
                listbox_item_types.insert(tk.END, item)
            listbox_item_types.pack(pady=10)

            def display_properties(event=None):
                '''
                显示物品类型的属性，点击物品类型时会显示该类型的属性。
                参数：
                event (tk.Event): 事件对象
                '''
                selected_index = listbox_item_types.curselection()
                selected_type = None
                if selected_index:
                    selected_type = listbox_item_types.get(selected_index)
                if selected_type:
                    # 获取选中物品类型的属性
                    item_types_data = self.load_item_types()
                    properties = item_types_data[selected_type]['properties']
                    new_type_name.set(selected_type)
                    # 清除之前的属性输入框
                    for widget in property_frame.winfo_children():
                        widget.destroy()
                    # 动态显示属性输入框
                    nonlocal property_vars
                    property_vars = []  # 清空属性输入框变量列表
                    for prop in properties:
                        property_var = tk.StringVar(value=prop)
                        property_input = tk.Entry(property_frame, textvariable=property_var)
                        property_input.pack(pady=5)
                        property_vars.append(property_var)

            def on_item_click(event=None):
                '''
                绑定选择事件，点击物品类型时会触发显示属性。
                参数：
                event (tk.Event): 事件对象
                '''
                display_properties(event) 

            listbox_item_types.bind('<<ListboxSelect>>', display_properties) 
            listbox_item_types.bind('<Button 1>', on_item_click)

            # 新物品类型信息输入框
            tk.Label(modify_window, text="物品类型:").pack(pady=5)
            new_type_name = tk.StringVar()
            entry_type_name = tk.Entry(modify_window, textvariable=new_type_name)
            entry_type_name.pack(pady=5)

            tk.Label(modify_window, text="物品属性:").pack(pady=5)
            property_frame = tk.Frame(modify_window)
            property_frame.pack(pady=10)

            btn_add_property = tk.Button(modify_window, text="添加属性", command=lambda: add_property_input(property_frame))
            btn_add_property.pack(pady=10)

            # 添加保存按钮
            btn_save_modify = tk.Button(modify_window, text="保存", command=save_modified_type)
            btn_save_modify.pack(pady=10)

            def add_property_input(frame):
                '''
                动态添加一个新的属性输入框。
                参数：
                frame (tk.Frame): 属性输入框的框架
                '''
                property_var = tk.StringVar()
                property_input = tk.Entry(frame, textvariable=property_var)
                property_input.pack(pady=5)
                property_vars.append(property_var)

        def update_item_types():
            '''
            更新物品类型列表，将所有物品类型显示到列表框中。
            '''
            listbox_item_types.delete(0, tk.END)
            item_types = list(self.load_item_types().keys())
            for item in item_types:
                listbox_item_types.insert(tk.END, item)

        def check_item_attribute():
            '''
            查看物品类型的属性，选择一个物品类型后会显示该类型的属性。
            '''
            selected_type = listbox_item_types.get(tk.ACTIVE)
            if selected_type:
                item_types = self.load_item_types()
                properties = item_types[selected_type]['properties']
                properties_text = "\n".join(properties)
                tk.messagebox.showinfo("物品属性", f"'{selected_type}' 的属性：\n{properties_text}")
                update_item_types()
            else:
                tk.messagebox.showerror("错误", "请选择要查看的物品类型")

        def view_items():
            '''
            查看物品列表，显示所有物品的名称，点击“修改信息”按钮可以修改物品信息，点击“删除物品”按钮可以删除物品。
            '''
            item_list_window = tk.Toplevel(admin_window)
            item_list_window.title('物品列表')
            item_listbox = tk.Listbox(item_list_window, width=20, height=20)
            item_listbox.pack(padx=10, pady=10)

            # 将物品名称添加到列表框中
            for item in self.item_info_data:
                item_listbox.insert(tk.END, item['物品名称'])

            modify_button = tk.Button(item_list_window, text="修改信息", command=lambda: modify_item(item_listbox))
            modify_button.pack(padx=10, pady=5)
            delete_button = tk.Button(item_list_window, text="删除物品", command=lambda: delete_item(item_listbox))
            delete_button.pack(padx=10, pady=5)

        def modify_item(item_listbox):
            '''
            修改物品信息，选择一个物品后可以修改物品的名称、描述、地址、联系方式等信息。
            输入框中显示原来的信息，修改后点击“保存修改”按钮保存修改。
            参数：
            item_listbox (tk.Listbox): 物品列表框
            '''
            selected_index = item_listbox.curselection()
            if not selected_index:
                tk.messagebox.showwarning("警告", "请选择一个物品")
                return

            selected_item = self.item_info_data[selected_index[0]]
            modify_window = tk.Toplevel(admin_window)
            modify_window.title("修改物品信息")
            entry_vars = {}
            row = 0

            for key, value in selected_item.items():
                if key != 'type' and key != 'properties':  # 忽略物品类型和属性
                    label = tk.Label(modify_window, text=key)
                    label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
                    entry_var = tk.StringVar(value=value)
                    entry = tk.Entry(modify_window, textvariable=entry_var)
                    entry.grid(row=row, column=1, padx=10, pady=5)
                    entry_vars[key] = entry_var
                    row += 1

            # 处理物品的属性
            if 'properties' in selected_item:
                properties = selected_item['properties']
                properties_vars = {}  
                property_frame = tk.Frame(modify_window)  
                property_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=5)

                tk.Label(property_frame, text="物品属性").grid(row=0, column=0, sticky="w", padx=10, pady=5)
                row += 1

                for prop_key, prop_value in properties.items():
                    prop_label = tk.Label(property_frame, text=prop_key)
                    prop_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
                    
                    prop_var = tk.StringVar(value=prop_value)
                    prop_entry = tk.Entry(property_frame, textvariable=prop_var)
                    prop_entry.grid(row=row, column=1, padx=10, pady=5)

                    properties_vars[prop_key] = prop_var
                    row += 1

                entry_vars['properties'] = properties_vars

            def save_changes():
                for key, entry_var in entry_vars.items():
                    if key == 'properties':  # 处理物品属性
                        updated_properties = {k: v.get() for k, v in entry_var.items()}
                        selected_item[key] = updated_properties
                    else:
                        selected_item[key] = entry_var.get()  

                # 保存更新后的数据
                self.item_info_data[selected_index[0]] = selected_item
                self.save_item_info()

                messagebox.showinfo("成功", "物品信息已更新")
                modify_window.destroy()  # 关闭修改窗口
        
            save_button = tk.Button(modify_window, text="保存修改", command=save_changes)
            save_button.grid(row=row, columnspan=2, pady=10)
            row += 1
            
        def delete_item(item_listbox):
            '''
            删除物品，选择一个物品后点击“删除物品”按钮可以删除物品。
            参数：
            item_listbox (tk.Listbox): 物品列表框
            '''
            selected_index = item_listbox.curselection()
            if not selected_index:
                tk.messagebox.showwarning("警告", "请选择一个物品")
                return
            item_name = self.item_info_data[selected_index[0]]['物品名称']
            confirmation = messagebox.askyesno("确认删除", f"确定要删除物品 '{item_name}' 吗？")
            # 如果用户确认删除
            if confirmation:
                self.item_info_data.pop(selected_index[0])
                self.save_item_info()
                tk.messagebox.showinfo("成功", f"物品 '{item_name}' 已删除！")
                item_listbox.delete(selected_index)

        def logout():
            '''
            退出管理员面板，返回登录窗口。
            '''
            admin_window.destroy()
            self.window.deiconify()  # 显示登录窗口

        btn_logout = tk.Button(admin_window, text="退出", command=logout)
        btn_logout.pack(pady=10)

        btn_view_items = tk.Button(admin_window, text="查看物品列表", command=view_items)
        btn_view_items.pack(pady=10)

        listbox_frame = tk.Frame(admin_window)
        listbox_frame.pack(pady=10)

        # 显示待审核用户列表
        tk.Label(listbox_frame, text="待审核用户列表").grid(row=0, column=0, padx=10, pady=10)
        self.user_listbox = tk.Listbox(listbox_frame, height=10, width=30)
        self.user_listbox.grid(row=1, column=0, padx=10, pady=10)

        # 显示物品类型列表
        tk.Label(listbox_frame, text="物品类型列表").grid(row=0, column=1, padx=10, pady=10)
        listbox_item_types = tk.Listbox(listbox_frame, height=10, width=30)
        listbox_item_types.grid(row=1, column=1, padx=10, pady=20)

        update_user_list()
        update_item_types()

        # 创建左侧按钮框架
        left_buttons_frame = tk.Frame(admin_window)
        left_buttons_frame.pack(side=tk.LEFT, padx=20, pady=10, fill = 'both')

        # 查看用户信息按钮
        btn_view_info = tk.Button(left_buttons_frame, text="查看用户信息", command=view_user_info)
        btn_view_info.pack(pady=5,padx = 70)

        # 审核通过/拒绝按钮
        btn_approve = tk.Button(left_buttons_frame, text="批准", command=approve_user)
        btn_approve.pack(pady=5)
        btn_reject = tk.Button(left_buttons_frame, text="拒绝", command=reject_user)
        btn_reject.pack(pady=5)

        # 查看用户名单
        btn_look_user = tk.Button(left_buttons_frame, text="查看用户列表", command=display_user_list)
        btn_look_user.pack(pady=5)

        # 创建右侧按钮框架
        right_buttons_frame = tk.Frame(admin_window)
        right_buttons_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill = 'both')

        # 物品类型管理按钮
        btn_attribute_info =  tk.Button(right_buttons_frame, text="查看属性", command=check_item_attribute)
        btn_attribute_info.pack(pady=5, padx = 70)
        
        btn_add_type = tk.Button(right_buttons_frame, text="添加物品类型", command=add_item_type)
        btn_add_type.pack(pady=5)

        btn_modify_type = tk.Button(right_buttons_frame, text="修改物品类型", command=modify_item_type)
        btn_modify_type.pack(pady=5)
        

    def user_panel(self, usr_name):
        '''
        用户面板：用户可以添加物品、查找物品。
        参数：
        usr_name (str): 用户名
        '''
        user_window = tk.Toplevel(self.window)
        user_window.title(f'{usr_name} 面板')
        user_window.geometry('400x500')

        # 定义物品名称、描述、地址等变量
        item_name_var = tk.StringVar()
        item_desc_var = tk.StringVar()
        item_address_var = tk.StringVar()
        item_phone_var = tk.StringVar()
        item_email_var = tk.StringVar()
        item_type_var = tk.StringVar()

        row = 0  
        tk.Label(user_window, text="物品名称").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_item_name = tk.Entry(user_window, textvariable=item_name_var)
        entry_item_name.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        tk.Label(user_window, text="物品描述").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_item_desc = tk.Entry(user_window, textvariable=item_desc_var)
        entry_item_desc.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        tk.Label(user_window, text="物品地址").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_item_address = tk.Entry(user_window, textvariable=item_address_var)
        entry_item_address.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        tk.Label(user_window, text="联系人手机").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_item_phone = tk.Entry(user_window, textvariable=item_phone_var)
        entry_item_phone.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        tk.Label(user_window, text="邮箱").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_item_email = tk.Entry(user_window, textvariable=item_email_var)
        entry_item_email.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        tk.Label(user_window, text="选择物品类别").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        item_types = list(self.load_item_types().keys())
        item_type_menu = tk.OptionMenu(user_window, item_type_var, *item_types)
        item_type_menu.grid(row=row, column=1, padx=10, pady=5)
        row += 1  

        # 用于动态展示属性输入框
        property_vars = []
        def update_properties(name, index, mode):
            '''
            更新物品属性输入框，根据选择的物品类别动态显示属性输入框。
            参数：
            name (str): 变量名
            index (int): 索引
            mode (str): 模式
            '''
            for widget in property_frame.winfo_children():
                widget.destroy()

            selected_type = item_type_var.get()
            if selected_type:
                # 获取物品类别的属性
                item_types_data = self.load_item_types()
                properties = item_types_data[selected_type]['properties']
                
                # 动态创建属性输入框
                nonlocal property_vars
                property_vars = []
                for i, prop in enumerate(properties):
                    # 创建属性的标签
                    property_label = tk.Label(property_frame, text=prop)
                    property_label.grid(row=i, column=0, padx=10, pady=5)  

                    # 创建属性的输入框
                    property_var = tk.StringVar()
                    property_input = tk.Entry(property_frame, textvariable=property_var)
                    property_input.grid(row=i, column=1, padx=10, pady=5)  
                    property_vars.append(property_var)

        # 物品属性输入框框架
        property_frame = tk.Frame(user_window)
        property_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        row += 1  
        # 监听物品类别选择变化，更新属性输入框
        item_type_var.trace('w', update_properties)

        def add_item():
            '''
            添加物品，点击“添加物品”按钮后将物品信息保存到文件中。
            '''
            item_name = item_name_var.get()
            item_desc = item_desc_var.get()
            item_address = item_address_var.get()
            item_phone = item_phone_var.get()
            item_email = item_email_var.get()
            item_type = item_type_var.get()

            # 检查是否填写了必填字段
            if not item_name or not item_desc or not item_address or not item_phone or not item_email or not item_type:
                tk.messagebox.showerror("错误", "所有字段必须填写！")
                return
            
            property_names = self.load_item_types()[item_type]['properties']
            properties = {property_names[i]: property_var.get() for i, property_var in enumerate(property_vars)}

            # 检查是否有空值
            if any(value == "" for value in properties.values()):
                tk.messagebox.showerror("错误", "所有属性字段必须填写！")
                return

            # 存储物品信息
            item_info = {
                '物品名称': item_name,
                '物品描述': item_desc,
                '物品地址': item_address,
                '联系人手机': item_phone,
                '邮箱': item_email,
                'type': item_type,
                'properties': properties
            }
            self.item_info_data.append(item_info)
            with open(self.item_info_file, "wb") as f:
                pickle.dump(self.item_info_data, f)
            tk.messagebox.showinfo("成功", f"物品 '{item_name}' 已成功添加！")

        btn_add_item = tk.Button(user_window, text="添加物品", command=add_item)
        btn_add_item.grid(row=row, column=1, padx=10, pady=5)
        row += 1    

        def search_item():
            '''
            搜索物品，弹出搜索窗口，用户可以选择物品类型和输入关键字搜索物品，如果找到匹配的物品则显示物品信息。
            匹配规则：物品名称和描述的相似度高于阈值则认为匹配成功。
            '''
            search_window = tk.Toplevel(self.window)
            search_window.title('搜索物品')
            search_window.geometry('500x300')

            # 选择物品类型
            item_type_var = tk.StringVar()
            item_types = list(self.load_item_types().keys())  # 获取物品类型
            tk.Label(search_window, text="选择物品类型").grid(row=0, column=0, padx=10, pady=5, sticky='w')
            item_type_menu = tk.OptionMenu(search_window, item_type_var, *item_types)
            item_type_menu.grid(row=0, column=1, padx=10, pady=5)

            # 输入搜索关键字
            keyword_var = tk.StringVar()
            tk.Label(search_window, text="请输入关键字（物品名称或描述）").grid(row=1, column=0, padx=10, pady=5, sticky='w')
            keyword_entry = tk.Entry(search_window, textvariable=keyword_var)
            keyword_entry.grid(row=1, column=1, padx=10, pady=5)

            def perform_search():
                '''
                执行搜索
                '''
                item_type = item_type_var.get()
                keyword = keyword_var.get()
                threshold = 50  # 相似度阈值
                if not item_type or not keyword:
                    tk.messagebox.showerror("错误", "物品类型和关键字不能为空！")
                    return

                all_items = self.load_item_info()
                filtered_items = []
                for item in all_items:
                    if item['type'] == item_type:
                        # 计算物品名称和关键字的相似度
                        name_match_score = fuzz.partial_ratio(keyword, item['物品名称'])
                        desc_match_score = fuzz.partial_ratio(keyword, item['物品描述'])
                        
                        # 如果相似度高于阈值，则认为匹配成功
                        if name_match_score >= threshold or desc_match_score >= threshold:
                            filtered_items.append(item)

                if filtered_items:
                    result_text = ""
                    for i, item in enumerate(filtered_items):
                        # 对于每个物品，按格式输出属性
                        item_info = f"物品 {i+1}: {item['物品名称']}" + "\n" + "\n".join([f"{key}: {value}" for key, value in item.items() if key != '物品名称' and key != 'type' and key != 'properties']) 
                        item_info = item_info + "\n" + "\n".join([f"{key}: {value}" for key, value in item['properties'].items()])
                        result_text += item_info + "\n\n"  
                    tk.messagebox.showinfo("搜索结果", result_text.strip())  # 去掉末尾的多余换行
                else:
                    tk.messagebox.showinfo("没有结果", "未找到符合条件的物品。")

            # 搜索按钮
            search_button = tk.Button(search_window, text="搜索", command=perform_search)
            search_button.grid(row=2, column=1, padx=10, pady=10)

        # 搜索物品按钮
        btn_search = tk.Button(user_window, text="搜索物品", command=search_item)
        btn_search.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        def logout():
            '''
            退出用户面板，返回登录窗口。
            '''
            user_window.destroy()  # 关闭用户面板
            self.window.deiconify()  # 显示登录窗口

        btn_logout = tk.Button(user_window, text="退出登录", command=logout)
        btn_logout.grid(row=row, column=1, padx=10, pady=5)
        
# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = ExchangeSystemApp(root)
    root.mainloop()