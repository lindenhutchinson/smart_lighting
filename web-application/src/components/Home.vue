<template>
  <div id="home">
     <li v-for="ctrl in controllers" :key="ctrl._id">{{ctrl}}</li>
  </div>
</template>

<script>


export default {
  name: "Home",
  components: {
  },
  data() {
    return {
      controllers: [],
    };
  },
  async mounted() {
    await this.getData();
  }, 
  methods: {
    async getData() {
      // try {
        const response = await this.$http.get("http://localhost:5000/");
        // JSON responses are automatically parsed.
        console.log(response);
        this.controllers = response.data;
      // } catch (error) {
      //   console.log(error);
      // }
    },

    // async addData() {
    //   try {
    //     const response = await this.$http.post("localhost:5000", {
          
    //     });
    //     // JSON responses are automatically parsed.
    //     console.log(response.data);
    //     this.data = response.data;
    //   } catch (error) {
    //     console.log(error);
    //   }
    // },
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
