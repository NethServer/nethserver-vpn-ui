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
    <div v-show="view.isLoaded">
      <div class="row">
        <h3>{{ $t('dashboard.ipsec_stats') }}</h3>
        <div class="stats-container col-xs-6 col-sm-6 col-md-6 col-lg-6">
          <span
            class="card-pf-utilization-card-details-count stats-count"
          >{{status.ipsec.connected}}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.ipsec_connected') }}</span>
          </span>
        </div>
        <div class="stats-container col-xs-6 col-sm-6 col-md-6 col-lg-6">
          <span class="card-pf-utilization-card-details-count stats-count">{{status.ipsec.total}}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.ipsec_total') }}</span>
          </span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="row">
        <h3>{{ $t('dashboard.openvpn_tun_stats') }}</h3>
        <div class="stats-container col-xs-6 col-sm-6 col-md-6 col-lg-6">
          <span
            class="card-pf-utilization-card-details-count stats-count"
          >{{status.openvpn.tunnels.connected}}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.openvpn_tun_connected') }}</span>
          </span>
        </div>
        <div class="stats-container col-xs-6 col-sm-6 col-md-6 col-lg-6">
          <span
            class="card-pf-utilization-card-details-count stats-count"
          >{{status.openvpn.tunnels.total}}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.openvpn_tun_total') }}</span>
          </span>
        </div>
        <!-- charts -->
        <h4>{{ $t('dashboard.openvpn_tun_interfaces') }}</h4>
        <div
          v-for="(i,ik) in status.openvpn.tunnels.interfaces"
          :key="ik"
          class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
        >
          <h5>{{i}}</h5>
          <div v-if="!charts[i]" class="spinner spinner-lg view-spinner"></div>
          <div
            v-if="charts[i] && charts[i].data && charts[i].data.length == 0"
            class="empty-piechart"
          >
            <span class="fa fa-line-chart"></span>
            <div>{{ $t('dashboard.empty_piechart_label') }}</div>
          </div>
          <div v-show="charts[i] && charts[i].data && charts[i].data.length > 0">
            <h4 class="col-sm-12">
              <div :id="'ovpn-tun-legend-'+i" class="legend"></div>
            </h4>
            <div :id="'ovpn-tun-chart-'+i" class="col-sm-12"></div>
          </div>
        </div>
        <!-- end charts -->
      </div>

      <div class="divider"></div>

      <div class="row">
        <h3>{{ $t('dashboard.openvpn_rw_stats') }}</h3>
        <div class="row">
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span class="card-pf-utilization-card-details-count stats-count">
              <span
                :class="status.openvpn.roadwarrior.status == 'enabled' ? 'fa fa-check green' : 'fa fa-times red'"
              ></span>
            </span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_status') }}</span>
            </span>
          </div>
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span
              class="card-pf-utilization-card-details-count stats-count"
            >{{status.openvpn.roadwarrior.connected}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_connected') }}</span>
            </span>
          </div>
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span
              class="card-pf-utilization-card-details-count stats-count"
            >{{status.openvpn.roadwarrior.total}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_total') }}</span>
            </span>
          </div>
        </div>
        <div class="row">
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span
              class="card-pf-utilization-card-details-count stats-count"
            >{{status.openvpn.roadwarrior.auth | capitalize}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_auth') }}</span>
            </span>
          </div>
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span
              class="card-pf-utilization-card-details-count stats-count"
            >{{status.openvpn.roadwarrior.mode | capitalize}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_mode') }}</span>
            </span>
          </div>
          <div class="stats-container col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <span
              class="card-pf-utilization-card-details-count stats-count"
            >{{status.openvpn.roadwarrior.port}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{ $t('dashboard.openvpn_rw_port') }}</span>
            </span>
          </div>
        </div>

        <div class="row margin-top-15">
        <!-- top traffic accounts -->
          <div class="width-33">
            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title">{{ $t('dashboard.openvpn_rw_top_traffic_accounts') }}</h3>
              </div>
              <div class="panel-body" v-for="item in status.openvpn.roadwarrior.topTrafficAccounts" :key="item.account">
                <span
                  class="card-pf-utilization-card-details-count stats-count-small col-xs-5"
                >{{ item.traffic | byteFormat}}</span>
                <span
                  class="card-pf-utilization-card-details-description stats-description-small col-xs-6"
                >
                  <span
                    class="card-pf-utilization-card-details-line-2 stats-text-small"
                  >{{ item.account }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="row">
          <!-- charts -->
          <h4>{{ $t('dashboard.openvpn_rw_interfaces') }}</h4>
          <div
            v-for="(i,ik) in status.openvpn.roadwarrior.interfaces"
            :key="ik"
            class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
          >
            <h5>{{i}}</h5>
            <div v-if="!charts[i]" class="spinner spinner-lg view-spinner"></div>
            <div
              v-if="charts[i] && charts[i].data && charts[i].data.length == 0"
              class="empty-piechart"
            >
              <span class="fa fa-line-chart"></span>
              <div>{{ $t('dashboard.empty_piechart_label') }}</div>
            </div>
            <div v-show="charts[i] && charts[i].data && charts[i].data.length > 0">
              <h4 class="col-sm-12">
                <div :id="'ovpn-rw-legend-'+i" class="legend"></div>
              </h4>
              <div :id="'ovpn-rw-chart-'+i" class="col-sm-12"></div>
            </div>
          </div>
          <!-- end charts -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
var nethserver = window.nethserver;
var console = window.console;

import Dygraph from "dygraphs";

export default {
  name: "Dashboard",
  beforeRouteLeave(to, from, next) {
    for (var i in this.charts) {
      if (this.charts[i].pollingId) {
        clearInterval(this.charts[i].pollingId);
      }
    }
    next();
  },
  mounted() {
    this.getStats();
  },
  data() {
    return {
      view: {
        isLoaded: false
      },
      status: {
        openvpn: {
          tunnels: {
            interfaces: [],
            connected: 0,
            total: 0
          },
          roadwarrior: {
            auth: "certificate",
            interfaces: [],
            mode: "routed",
            status: "enabled",
            connected: 0,
            port: 0,
            total: 0,
            topTrafficAccounts: []
          }
        },
        ipsec: {
          connected: 0,
          total: 0
        }
      },
      charts: {},
      tableLangsTexts: this.tableLangs()
    };
  },
  methods: {
    initCharts(chartName, type) {
      var context = this;

      context.view.isChartLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/dashboard/read"],
        {
          action: "chart",
          name: chartName
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }

          if (success.data && success.data.length > 0) {
            for (var t in success.data) {
              success.data[t][0] = new Date(success.data[t][0] * 1000);
            }

            context.charts[chartName] = new Dygraph(
              document.getElementById("ovpn-" + type + "-chart-" + chartName),
              success.data.reverse(),
              {
                fillGraph: true,
                stackedGraph: true,
                labels: success.labels,
                height: 150,
                strokeWidth: 1,
                strokeBorderWidth: 1,
                ylabel:
                  (context.$i18n && context.$i18n.t("dashboard.bytes")) ||
                  "Bytes",
                axisLineColor: "white",
                labelsDiv: document.getElementById(
                  "ovpn-" + type + "-legend-" + chartName
                ),
                labelsSeparateLines: true,
                legend: "always",
                axes: {
                  y: {
                    axisLabelFormatter: function(y) {
                      return context.$options.filters.byteFormat(y);
                    }
                  }
                }
              }
            );
            context.charts[chartName].data = success.data;

            setTimeout(function() {
              context.charts[chartName].resize();
            }, 100);

            // start polling
            if (!context.charts[chartName].pollingId) {
              context.charts[chartName].pollingId = setInterval(function() {
                context.updateCharts(chartName, type);
              }, 5000);
            }
            context.$forceUpdate();
          } else {
            context.charts[chartName] = {
              data: []
            };
            context.$forceUpdate();
          }
        },
        function(error) {
          console.error(error);
          context.view.isChartLoaded = true;
        }
      );
    },
    updateCharts(chartName) {
      var context = this;
      nethserver.exec(
        ["nethserver-vpn/dashboard/read"],
        {
          action: "chart",
          name: chartName
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          if (success.data.length > 0) {
            for (var t in success.data) {
              success.data[t][0] = new Date(success.data[t][0] * 1000);
            }

            context.charts[chartName].updateOptions({
              file: success.data.reverse()
            });
          } else {
            context.charts[chartName] = {
              data: []
            };
            context.$forceUpdate();
          }
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getStats() {
      var context = this;

      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/dashboard/read"],
        {
          action: "status"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.status = success;

          for (var i in success.openvpn.tunnels.interfaces) {
            var name = success.openvpn.tunnels.interfaces[i];
            context.initCharts(name, "tun");
          }

          for (var i in success.openvpn.roadwarrior.interfaces) {
            var name = success.openvpn.roadwarrior.interfaces[i];
            context.initCharts(name, "rw");
          }

          context.view.isLoaded = true;
          context.$forceUpdate();
        },
        function(error) {
          console.error(error);
        }
      );
    }
  }
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

.status-body {
  font-size: 14px;
}

.row {
  padding-left: 20px;
  padding-right: 20px;
}

.semi-bold {
  font-weight: 500;
}

.stats-count-small {
  margin-right: 5px;
  font-size: 18px;
  font-weight: 300;
  float: left;
  line-height: 0.5;
}

.stats-text-small {
  line-height: 0.5;
}

.legend {
  z-index: 5;
}

.stats-description-small {
  float: left;
  overflow: hidden;
  text-overflow: ellipsis;
}

.divider {
  margin-top: 20px;
}

.margin-top-15 {
  margin-top: 15px;
}

.width-33 {
  width: 33%;
}

</style>
