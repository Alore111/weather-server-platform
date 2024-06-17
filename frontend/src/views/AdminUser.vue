<template>
    <div>
        <el-button type="primary" @click="showAddUserForm">添加用户</el-button>
        <el-table :data="users" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="50"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="qq" label="QQ"></el-table-column>
            <el-table-column label="操作" width="180">
                <template #default="scope">
                    <el-button size="mini" @click="editUser(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="deleteUser(scope.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog :title="isEdit ? '编辑用户' : '添加用户'" v-model="dialogVisible">
            <el-form :model="selectedUser" label-width="120px">
                <el-form-item label="用户名">
                    <el-input v-model="selectedUser.username"></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input type="password" v-model="selectedUser.password"></el-input>
                </el-form-item>
                <el-form-item label="QQ">
                    <el-input v-model="selectedUser.qq"></el-input>
                </el-form-item>
                <el-form-item label="角色">
                    <el-select v-model="selectedUser.role_id">
                        <el-option label="用户" :value="1"></el-option>
                        <el-option label="管理员" :value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm">提交</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    data() {
        return {
            users: [],
            loading: false,
            dialogVisible: false,
            selectedUser: {
                username: '',
                password: '',
                qq: '',
                role_id: 1
            },
            isEdit: false
        };
    },
    methods: {
        async fetchUsers() {
            this.loading = true;
            try {
                const response = await fetch(`${this.$serverUrl}/api/get_all_users`);
                const data = await response.json();
                if (response.ok) {
                    this.users = data.users;
                } else {
                    ElMessage.error(data.message || '获取用户失败');
                }
            } catch (error) {
                console.error('Error fetching users:', error);
                ElMessage.error('获取用户失败');
            } finally {
                this.loading = false;
            }
        },
        showAddUserForm() {
            this.selectedUser = { username: '', password: '', qq: '', role_id: 1 };
            this.isEdit = false;
            this.dialogVisible = true;
        },
        editUser(user) {
            this.selectedUser = { ...user, password: '' };  // 清除密码字段，确保安全性
            this.isEdit = true;
            this.dialogVisible = true;
        },
        async deleteUser(userId) {
            try {
                const response = await fetch(`${this.$serverUrl}/api/delete_user`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ user_id: userId })
                });
                const result = await response.json();
                if (response.ok) {
                    ElMessage.success('删除成功');
                    this.fetchUsers();
                } else {
                    ElMessage.error(result.message || '删除失败');
                }
            } catch (error) {
                console.error('Error deleting user:', error);
                ElMessage.error('删除失败');
            }
        },
        async submitForm() {
            const url = this.isEdit ? `${this.$serverUrl}/api/update_user` : `${this.$serverUrl}/api/add_user`;
            const method = 'POST';
            const headers = {
                'Content-Type': 'application/json'
            };
            const body = JSON.stringify(this.selectedUser);

            try {
                const response = await fetch(url, { method, headers, body });
                const result = await response.json();
                if (response.ok) {
                    ElMessage.success(this.isEdit ? '更新成功' : '添加成功');
                    this.dialogVisible = false;
                    this.fetchUsers();
                } else {
                    ElMessage.error(result.message || '操作失败');
                }
            } catch (error) {
                console.error('Error submitting form:', error);
                ElMessage.error(this.isEdit ? '更新失败' : '添加失败');
            }
        }
    },
    mounted() {
        this.fetchUsers();
    }
};
</script>

<style scoped>
/* 你可以在这里添加组件特定的样式 */
</style>