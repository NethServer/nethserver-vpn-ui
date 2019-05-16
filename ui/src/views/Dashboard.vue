<!--
/*
 * Copyright (C) 2019 Nethesis S.r.l.
 * http://www.nethesis.it - nethserver@nethesis.it
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see COPYING.
 */
-->

<template>
  <div>
    <h2>{{ $t('dashboard.title') }}</h2>

    <div v-if="!view.isLoaded" class="spinner spinner-lg view-spinner"></div>
    <div v-show="view.isLoaded"></div>
  </div>
</template>

<script>
var nethserver = window.nethserver;
var console = window.console;

import generatePieChart from "@/piechart";

export default {
  name: "Dashboard",
  mounted() {},
  data() {
    return {
      view: {
        isLoaded: false
      }
    };
  },
  methods: {}
};
</script>

<style scoped>
.no-mg-top {
  margin-top: 0px !important;
}
.min-size {
  font-size: 14px;
}

.empty-piechart {
  margin-top: 2em;
  text-align: center;
  color: #9c9c9c;
}

.empty-piechart .fa {
  font-size: 92px;
  color: #bbbbbb;
}

.mg-bottom-10 {
  margin-bottom: 10px;
}
</style>
