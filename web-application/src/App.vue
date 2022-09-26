<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <button @click="addController">Create Controller</button>
    <table>
      <thead>
        <td>ID</td>
        <td>Brightness</td>
        <td>Last Update</td>
        <td>Actions</td>
      </thead>
      <tbody>
        <tr v-for="ctrl in controllers" :key="ctrl._id"> 
          <td>{{ctrl._id}}</td>
          <td>{{ctrl.brightness}}</td>
          <td>{{new Date(ctrl.last_motion_detected*1000).toLocaleString()}}</td>
          <td><button>ON</button></td>
        </tr>
      </tbody>

    </table>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  data() {
    return {
      controllers: [],
    };
  },
  async mounted() {
    await this.getData();
  },
  computed: {
    getControllers: () => this.controllers
  },
  methods: {
    async getData() {
      try {
        const response = await this.$http.get("http://localhost:5000/");
        // JSON responses are automatically parsed.
        console.log(response);
        this.controllers = response.data;
      } catch (error) { 
        console.log(error);
      }
    },

    async addController() {
      // try {
        const response = await this.$http.post("http://localhost:5000/ctrl/create", {});
        // JSON responses are automatically parsed.
        console.log(response.data);
        this.controllers = [...this.controllers, response.data];
      // } catch (error) {
      //   console.log(error);
      // }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
