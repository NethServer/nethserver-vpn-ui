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
    <h2>{{ $t('openvpn_rw.title') }}</h2>

    <div v-if="!view.isLoaded" class="spinner spinner-lg view-spinner"></div>

    <div v-show="!view.menu.installed && view.isLoaded">
      <div class="blank-slate-pf" id>
        <div class="blank-slate-pf-icon">
          <span class="pficon pficon pficon-add-circle-o"></span>
        </div>
        <h1>{{$t('package_required')}}</h1>
        <p>{{$t('package_required_desc')}}.</p>
        <pre>{{view.menu.packages.join(' ')}}</pre>
        <div class="blank-slate-pf-main-action">
          <button
            :disabled="view.isInstalling"
            @click="installPackages()"
            class="btn btn-primary btn-lg"
          >{{view.menu.packages.length == 1 ? $t('install_package') : $t('install_packages')}}</button>
          <div v-if="view.isInstalling" class="spinner spinner-sm"></div>
        </div>
      </div>
    </div>

    <div v-show="view.menu.installed && view.isLoaded">
      <h3>{{ $t('openvpn_rw.rw_server') }}</h3>

      <div v-if="configuration.status == 'disabled'" class="blank-slate-pf">
        <h1>{{$t('openvpn_rw.openvpn_rw_server_is_disabled')}}</h1>
        <p>{{$t('openvpn_rw.openvpn_rw_server_is_disabled_desc')}}.</p>
        <div class="blank-slate-pf-main-action">
          <button
            v-if="configuration.status == 'disabled'"
            @click="toggleStatus(false)"
            class="btn btn-primary btn-lg"
          >{{$t('openvpn_rw.enable_openvpn_rw_server')}}</button>
        </div>
      </div>

      <div v-show="configuration.status == 'enabled'" class="panel panel-default">
        <div class="panel-heading">
          <button
            v-if="configuration.status == 'enabled'"
            :disabled="configuration.status == 'disabled'"
            @click="toggleStatus(true)"
            class="btn btn-primary right proxy-details"
          >{{$t('edit')}}</button>
          <toggle-button
            class="min-toggle right"
            :width="40"
            :height="20"
            :color="{checked: '#0088ce', unchecked: '#bbbbbb'}"
            :value="configuration.status == 'enabled'"
            :sync="true"
            @change="toggleStatus(false)"
          />

          <span class="panel-title">
            {{$t('openvpn_rw.enabled')}}
            <span
              :class="['fa', configuration.status == 'enabled' ? 'fa-check green' : 'fa-times red']"
            ></span>

            <span class="handle-overflow span-left-margin semi-bold color-link-hover">
              <span class="semi-bold">{{$t('openvpn_rw.auth_mode')}}:</span>
              <b class="span-left-margin">{{$t('openvpn_rw.'+mapAuthMode(configuration.AuthMode))}}</b>
            </span>
          </span>
        </div>
      </div>

      <h3>{{ $t('actions') }}</h3>
      <button
        @click="openCreateAccount()"
        class="btn btn-primary btn-lg"
      >{{$t('openvpn_rw.add_account')}}</button>

      <h3>{{ $t('openvpn_rw.rw_accounts') }}</h3>
      <vue-good-table
        :customRowsPerPageDropdown="[25,50,100]"
        :perPage="25"
        :columns="accountsColumns"
        :rows="accounts"
        :lineNumbers="false"
        :defaultSortBy="{field: 'name', type: 'asc'}"
        :globalSearch="true"
        :paginate="true"
        styleClass="table"
        :nextText="tableLangsTexts.nextText"
        :prevText="tableLangsTexts.prevText"
        :rowsPerPageText="tableLangsTexts.rowsPerPageText"
        :globalSearchPlaceholder="tableLangsTexts.globalSearchPlaceholder"
        :ofText="tableLangsTexts.ofText"
      >
        <template slot="table-row" slot-scope="props">
          <td :class="['fancy', props.row.status == 'disabled' ? 'gray': '']">
            <a
              :class="props.row.status == 'disabled' ? 'gray': ''"
              @click="openEditAccount(props.row)"
            >
              <strong>{{ props.row.ShortName}}</strong>
            </a>
          </td>
          <td :class="['fancy', props.row.status == 'disabled' ? 'gray': '']">
            <span :class="['pficon', props.row.Mode == 'system' ? ' pficon-user' : 'pficon-key']"></span>
            <span class="span-left-margin">{{$t("openvpn_rw."+props.row.Mode+'_mode') }}</span>
          </td>
          <td
            :class="['fancy', props.row.status == 'disabled' ? 'gray': '']"
          >{{props.row.Expiration ? (props.row.Expiration + " (" + $t("openvpn_rw."+props.row.CertificateStatus+'_status') + ")") : "-" }}</td>
          <td
            :class="['fancy', props.row.status == 'disabled' ? 'gray': '']"
          >{{ props.row.OpenVpnIp || '-'}} {{props.row.Host ? "("+props.row.Host+")" : ''}}</td>
          <td
            :class="['fancy', props.row.status == 'disabled' ? 'gray': '']"
          >{{ props.row.VPNRemoteNetwork ? (props.row.VPNRemoteNetwork + "/" + props.row.VPNRemoteNetmask) : '-' }}</td>
          <td :class="['fancy', props.row.status == 'disabled' ? 'gray': '']">
            <div
              v-if="props.row.statistics"
              data-toggle="tooltip"
              data-placement="top"
              data-html="true"
              :title="showStatistics(props.row.statistics)"
              class="handle-overflow"
            >
              <span class="fa fa-check green"></span>
              {{$t('openvpn_rw.connected')}} ({{props.row.statistics.virtual_address}})
            </div>
            <div v-else>
              <span class="fa fa-times grey"></span>
              {{$t('openvpn_rw.not_connected')}}
            </div>
          </td>

          <td :class="['fancy', props.row.status == 'disabled' ? 'gray': '']">
            <a href="#"
              v-if="props.row.lastConnected"
              :class="props.row.status == 'disabled' ? 'gray': ''"
              :title="$t('openvpn_rw.connection_history')"
              @click="showConnectionHistory(props.row.name, 'today')"
            >
              {{ props.row.lastConnected | dateFormat }}
            </a>
            <span v-else>-</span>
          </td>

          <td>
            <button
              @click="props.row.status == 'disabled' ? toggleStatusAccount(props.row) : openEditAccount(props.row)"
              :class="['btn btn-default', props.row.status == 'disabled' ? 'btn-primary' : '']"
            >
              <span
                :class="['fa', props.row.status == 'disabled' ? 'fa-check' : 'fa-pencil', 'span-right-margin']"
              ></span>
              {{props.row.status == 'disabled' ? $t('enable') : $t('edit')}}
            </button>
            <div class="dropup pull-right dropdown-kebab-pf">
              <button
                class="btn btn-link dropdown-toggle"
                type="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="true"
              >
                <span class="fa fa-ellipsis-v"></span>
              </button>
              <ul class="dropdown-menu dropdown-menu-right">
                <li>
                  <a @click="openDownloadAccount(props.row)">
                    <span class="fa fa-arrow-down span-right-margin"></span>
                    {{$t('download')}}
                  </a>
                </li>
                <li>
                  <a @click="openSendEmailAccount(props.row)">
                    <span class="fa fa-envelope span-right-margin"></span>
                    {{$t('openvpn_rw.send_with_email')}}
                  </a>
                </li>
                <li>
                  <a @click="toggleStatusAccount(props.row)">
                    <span
                      :class="['fa', props.row.status == 'enabled' ? 'fa-lock' : 'fa-check', 'span-right-margin']"
                    ></span>
                    {{props.row.status == 'enabled' ? $t('disable') : $t('enable')}}
                  </a>
                </li>
                <li role="presentation" class="divider"></li>
                <li v-if="props.row.statistics">
                  <a @click="openKillAccount(props.row)">
                    <span class="fa fa-times-circle span-right-margin"></span>
                    {{$t('openvpn_rw.kill')}}
                  </a>
                </li>
                <li>
                  <a @click="openDeleteAccount(props.row)">
                    <span class="fa fa-times span-right-margin"></span>
                    {{$t('delete')}}
                  </a>
                </li>
              </ul>
            </div>
          </td>
        </template>
      </vue-good-table>
    </div>

    <!-- MODALS -->
    <div class="modal" id="configureRWModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_rw.configure_rw_server')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveConfiguration(newConfiguration)">
            <div class="modal-body">
              <div
                :class="['form-group', newConfiguration.errors.AuthMode.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.auth_mode')}}</label>
                <div class="col-sm-9">
                  <select class="form-control" v-model="newConfiguration.AuthMode">
                    <option value="password">{{$t('openvpn_rw.username_password')}}</option>
                    <option value="certificate">{{$t('openvpn_rw.certificate')}}</option>
                    <option
                      value="password-certificate"
                    >{{$t('openvpn_rw.username_password_certificate')}}</option>
                  </select>
                  <span
                    v-if="newConfiguration.errors.AuthMode.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.AuthMode.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', newConfiguration.errors.Mode.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.mode')}}</label>
                <div class="col-sm-9">
                  <select v-model="newConfiguration.Mode" class="form-control">
                    <option value="routed">{{$t('openvpn_rw.routed')}}</option>
                    <option value="bridged">{{$t('openvpn_rw.bridged')}}</option>
                  </select>
                  <span
                    v-if="newConfiguration.errors.Mode.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Mode.message)}}</span>
                </div>
              </div>

              <div
                v-if="newConfiguration.Mode == 'routed'"
                :class="['form-group', newConfiguration.errors.Network.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.network')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="newConfiguration.Network" class="form-control">
                  <span
                    v-if="newConfiguration.errors.Network.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Network.message)}}</span>
                </div>
              </div>
              <div
                v-if="newConfiguration.Mode == 'routed'"
                :class="['form-group', newConfiguration.errors.Netmask.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.netmask')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="newConfiguration.Netmask" class="form-control">
                  <span
                    v-if="newConfiguration.errors.Netmask.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Netmask.message)}}</span>
                </div>
              </div>

              <div
                v-if="newConfiguration.Mode == 'bridged'"
                :class="['form-group', newConfiguration.errors.BridgeName.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.bridge')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.BridgeName" class="form-control">
                    <option
                      v-for="(i,ik) in interfaces"
                      :key="ik"
                      :value="i.name"
                    >{{i.name}} - {{i.address | uppercase}}</option>
                  </select>
                  <span
                    v-if="newConfiguration.errors.BridgeName.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.BridgeName.message)}}</span>
                </div>
              </div>
              <div
                v-if="newConfiguration.Mode == 'bridged'"
                :class="['form-group', newConfiguration.errors.BridgeStartIP.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.bridge_start_ip')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="newConfiguration.BridgeStartIP" class="form-control">
                  <span
                    v-if="newConfiguration.errors.BridgeStartIP.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.BridgeStartIP.message)}}</span>
                </div>
              </div>
              <div
                v-if="newConfiguration.Mode == 'bridged'"
                :class="['form-group', newConfiguration.errors.BridgeEndIP.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.bridge_end_ip')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="newConfiguration.BridgeEndIP" class="form-control">
                  <span
                    v-if="newConfiguration.errors.BridgeEndIP.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.BridgeEndIP.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', newConfiguration.errors.Remote.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.remote_host_ip_name')}}</label>
                <div class="col-sm-9">
                  <textarea
                    type="text"
                    v-model="newConfiguration.Remote"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="newConfiguration.errors.Remote.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Remote.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span
                  :class="['fa fa-angle-right field-section-toggle-pf', newConfiguration.advanced ? 'fa-angle-down' : '']"
                ></span>
                <a
                  class="field-section-toggle-pf"
                  @click="toggleAdvancedConfiguration()"
                >{{$t('advanced_mode')}}</a>
              </legend>

              <legend
                v-show="newConfiguration.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.connection_params')}}</span>
              </legend>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.Protocol.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.protocol')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.Protocol" class="form-control">
                    <option value="udp">{{$t('openvpn_rw.udp')}}</option>
                    <option value="tcp">{{$t('openvpn_rw.tcp')}}</option>
                  </select>
                  <span
                    v-if="newConfiguration.errors.Protocol.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Protocol.message)}}</span>
                </div>
              </div>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.Port.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.port')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="newConfiguration.Port" class="form-control">
                  <span
                    v-if="newConfiguration.errors.Port.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Port.message)}}</span>
                </div>
              </div>

              <legend
                v-show="newConfiguration.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.security_params')}}</span>
              </legend>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.Compression.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.compress')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.Compression" class="form-control">
                    <option value="disabled">{{$t('openvpn_rw.disabled')}}</option>
                    <option value="lzo">{{$t('openvpn_rw.lzo')}}</option>
                    <option value="lz4">{{$t('openvpn_rw.lz4')}}</option>
                  </select>
                  <span
                    v-if="newConfiguration.errors.Compression.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.Compression.message)}}</span>
                </div>
              </div>
              <div v-show="newConfiguration.advanced" class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.digest')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.Digest" class="form-control">
                    <option
                      v-for="(i,ik) in digests"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>
              <div v-show="newConfiguration.advanced" class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.cipher')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.Cipher" class="form-control">
                    <option
                      v-for="(i,ik) in ciphers"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>
              <div v-show="newConfiguration.advanced" class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.tls_min_version')}}</label>
                <div class="col-sm-7">
                  <select v-model="newConfiguration.TlsVersionMin" class="form-control">
                    <option value>{{$t('openvpn_tun.auto')}}</option>
                    <option value="1.1">1.1</option>
                    <option value="1.2">1.2</option>
                  </select>
                </div>
              </div>

              <div
                v-if="newConfiguration.Mode == 'routed'"
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.ClientToClient.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.client_to_client')}}</label>
                <div class="col-sm-7">
                  <input
                    type="checkbox"
                    v-model="newConfiguration.ClientToClient"
                    class="form-control"
                    true-value="enabled"
                    false-value="disabled"
                  >
                  <span
                    v-if="newConfiguration.errors.ClientToClient.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.ClientToClient.message)}}</span>
                </div>
              </div>

              <legend
                v-show="newConfiguration.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.routes_params')}}</span>
              </legend>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.PushExtraRoutes.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.push_static_routes')}}</label>
                <div class="col-sm-7">
                  <input
                    type="checkbox"
                    v-model="newConfiguration.PushExtraRoutes"
                    class="form-control"
                    true-value="enabled"
                    false-value="disabled"
                  >
                  <span
                    v-if="newConfiguration.errors.PushExtraRoutes.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.PushExtraRoutes.message)}}</span>
                </div>
              </div>

              <div
                v-show="newConfiguration.advanced"
                v-if="newConfiguration.Mode == 'routed'"
                :class="['form-group', newConfiguration.errors.RouteToVPN.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.route_traffic_to_vpn')}}</label>
                <div class="col-sm-7">
                  <input
                    type="checkbox"
                    v-model="newConfiguration.RouteToVPN"
                    true-value="enabled"
                    false-value="disabled"
                    class="form-control"
                  >
                  <span
                    v-if="newConfiguration.errors.RouteToVPN.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.RouteToVPN.message)}}</span>
                </div>
              </div>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.CustomRoutes.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.custom_routes')}}</label>
                <div class="col-sm-7">
                  <textarea
                    type="text"
                    v-model="newConfiguration.CustomRoutes"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="newConfiguration.errors.CustomRoutes.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.CustomRoutes.message)}}</span>
                </div>
              </div>

              <legend
                v-show="newConfiguration.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.extra_params')}}</span>
              </legend>

              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.PushDomain.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.dhcp_domain')}}</label>
                <div class="col-sm-9">
                  <input type="text" v-model="newConfiguration.PushDomain" class="form-control">
                  <span
                    v-if="newConfiguration.errors.PushDomain.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.PushDomain.message)}}</span>
                </div>
              </div>
              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.PushDns.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.dhcp_dns')}}</label>
                <div class="col-sm-9">
                  <input type="text" v-model="newConfiguration.PushDns" class="form-control">
                  <span
                    v-if="newConfiguration.errors.PushDns.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.PushDns.message)}}</span>
                </div>
              </div>
              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.PushWins.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.dhcp_wins')}}</label>
                <div class="col-sm-9">
                  <input type="text" v-model="newConfiguration.PushWins" class="form-control">
                  <span
                    v-if="newConfiguration.errors.PushWins.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.PushWins.message)}}</span>
                </div>
              </div>
              <div
                v-show="newConfiguration.advanced"
                :class="['form-group', newConfiguration.errors.PushNbdd.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.dhcp_nbdd')}}</label>
                <div class="col-sm-9">
                  <input type="text" v-model="newConfiguration.PushNbdd" class="form-control">
                  <span
                    v-if="newConfiguration.errors.PushNbdd.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+newConfiguration.errors.PushNbdd.message)}}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div v-if="newConfiguration.isLoading" class="spinner spinner-sm form-spinner-loader"></div>
              <button
                @click="resetConfiguration()"
                class="btn btn-default"
                type="button"
                data-dismiss="modal"
              >{{$t('cancel')}}</button>
              <button
                class="btn btn-primary"
                type="submit"
              >{{newConfiguration.isEdit ? $t('edit') : $t('save')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal" id="createAccountModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{currentAccount.isEdit ? $t('openvpn_rw.edit_account') + ' '+ currentAccount.name : $t('openvpn_rw.add_account')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveAccount(currentAccount)">
            <div class="modal-body">
              <div
                :class="['form-group', currentAccount.errors.Mode.hasError ? 'has-error' : '']"
                v-if="!currentAccount.isEdit && configuration.AccountProvider"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.mode')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentAccount.Mode" class="form-control">
                    <option value="vpn">{{$t('openvpn_rw.vpn_only')}}</option>
                    <option value="system">{{$t('openvpn_rw.system_user')}}</option>
                  </select>
                  <span
                    v-if="currentAccount.errors.Mode.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.Mode.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentAccount.Mode == 'vpn' && !currentAccount.isEdit"
                :class="['form-group', currentAccount.errors.name.hasError ? 'has-error' : '']"
              >
                <label
                  :class="[ configuration.AccountProvider? 'col-sm-5' : 'col-sm-3', 'control-label']"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.username')}}</label>
                <div :class=" configuration.AccountProvider ? 'col-sm-7' : 'col-sm-9'">
                  <input required type="text" v-model="currentAccount.name" class="form-control">
                  <span
                    v-if="currentAccount.errors.name.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.name.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentAccount.Mode == 'system' && !currentAccount.isEdit && configuration.AccountProvider"
                :class="['form-group', currentAccount.errors.name.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.user')}}</label>
                <div class="col-sm-7">
                  <select required v-model="currentAccount.name" class="form-control">
                    <option
                      v-for="(u,uk) in users"
                      :key="uk"
                      :value="u.name"
                    >{{u.shortname}} ({{u.gecos}})</option>
                  </select>
                  <span
                    v-if="currentAccount.errors.name.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.name.message)}}</span>
                </div>
              </div>

              <legend
                class="fields-section-header-pf"
                aria-expanded="true"
                v-if="!currentAccount.isEdit"
              >
                <span
                  :class="['fa fa-angle-right field-section-toggle-pf', currentAccount.advanced ? 'fa-angle-down' : '']"
                ></span>
                <a
                  class="field-section-toggle-pf"
                  @click="toggleAdvancedAccount()"
                >{{$t('advanced_mode')}}</a>
              </legend>

              <legend
                v-if="currentAccount.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.dhcp_params')}}</span>
              </legend>
              <div
                :class="['form-group', currentAccount.errors.OpenVpnIp.hasError ? 'has-error' : '']"
                v-if="currentAccount.advanced"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.reserved_ip')}}</label>
                <div class="col-sm-9">
                  <input type="text" v-model="currentAccount.OpenVpnIp" class="form-control">
                  <span
                    v-if="currentAccount.errors.OpenVpnIp.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.OpenVpnIp.message)}}</span>
                </div>
              </div>

              <legend
                v-if="currentAccount.advanced"
                class="fields-section-header-pf"
                aria-expanded="true"
              >
                <span class="field-section-toggle-pf">{{$t('openvpn_rw.remote_network')}}</span>
              </legend>
              <div
                :class="['form-group', currentAccount.errors.VPNRemoteNetwork.hasError ? 'has-error' : '']"
                v-if="currentAccount.advanced"
              >
                <label class="col-sm-3 control-label" for="textInput-modal-markup">
                  {{$t('openvpn_rw.vpn_remote_network')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('openvpn_rw.vpn_remote_network')"
                    :chapter="'vpn_remote_network'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-9">
                  <input type="text" v-model="currentAccount.VPNRemoteNetwork" class="form-control">
                  <span
                    v-if="currentAccount.errors.VPNRemoteNetwork.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.VPNRemoteNetwork.message)}}</span>
                </div>
              </div>
              <div
                :class="['form-group', currentAccount.errors.VPNRemoteNetmask.hasError ? 'has-error' : '']"
                v-if="currentAccount.advanced"
              >
                <label class="col-sm-3 control-label" for="textInput-modal-markup">
                  {{$t('openvpn_rw.vpn_remote_netmask')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('openvpn_rw.vpn_remote_netmask')"
                    :chapter="'vpn_remote_netmask'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-9">
                  <input type="text" v-model="currentAccount.VPNRemoteNetmask" class="form-control">
                  <span
                    v-if="currentAccount.errors.VPNRemoteNetmask.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentAccount.errors.VPNRemoteNetmask.message)}}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div v-if="currentAccount.isLoading" class="spinner spinner-sm form-spinner-loader"></div>
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button
                class="btn btn-primary"
                type="submit"
              >{{currentAccount.isEdit ? $t('edit') : $t('save')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal" id="deleteAccountModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_rw.delete_account')}} {{toDeleteAccount.name}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="deleteAccount(toDeleteAccount)">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('are_you_sure')}}?</label>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button class="btn btn-danger" type="submit">{{$t('delete')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal" id="killAccountModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_rw.kill_account')}} {{toKillAccount.name}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="killAccount(toKillAccount)">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('are_you_sure')}}?</label>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button class="btn btn-danger" type="submit">{{$t('openvpn_rw.kill')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal" id="downloadAccountModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{$t('openvpn_rw.download_configuration')}} {{toDownloadAccount.ShortName}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="undefined">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-7 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.ovpn_download')}}</label>
                <div class="col-sm-5 control-div" for="textInput-modal-markup">
                  <button
                    @click="downloadAccount(toDownloadAccount.name, 'ovpn')"
                    class="btn btn-primary"
                    type="button"
                  >{{$t('download')}}</button>
                </div>
              </div>

              <div
                class="form-group"
                v-show="configuration.AuthMode == 'certificate' || configuration.AuthMode == 'certificate-password'"
              >
                <label
                  class="col-sm-7 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.pem_download')}}</label>
                <div class="col-sm-5 control-div" for="textInput-modal-markup">
                  <button
                    @click="downloadAccount(toDownloadAccount.name, 'pem')"
                    class="btn btn-primary"
                    type="button"
                  >{{$t('download')}}</button>
                </div>
              </div>

              <div
                class="form-group"
                v-show="configuration.AuthMode == 'certificate' || configuration.AuthMode == 'certificate-password'"
              >
                <label
                  class="col-sm-7 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.pkcs12_download')}}</label>
                <span class="col-sm-7 control-label">
                  {{$t('openvpn_rw.pkcs12_password')}}:
                  <tt>{{toDownloadAccount.name}}</tt>
                </span>
                <div class="col-sm-5 control-div" for="textInput-modal-markup">
                  <button
                    @click="downloadAccount(toDownloadAccount.name, 'pkcs12')"
                    class="btn btn-primary"
                    type="button"
                  >{{$t('download')}}</button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div
      class="modal"
      id="sendEmailAccountModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_rw.send_email_configuration')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="sendEmailAccount()">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_rw.address')}}</label>
                <div class="col-sm-9 control-div" for="textInput-modal-markup">
                  <input class="form-control" type="email" v-model="toSendEmailAccount.address">
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button class="btn btn-primary" type="submit">{{$t('openvpn_rw.send')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div
      class="modal"
      id="connectionHistoryModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog width-800">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_rw.connection_history_of')}} {{ connectionHistoryAccount }}</h4>
          </div>
          <form class="form-horizontal">
            <div class="modal-body text-center">
              <div v-if="!connectionHistory[connectionHistoryInterval][connectionHistoryAccount]" class="spinner spinner-sm form-spinner-loader"></div>
              <div v-else>
                <ul class="nav nav-tabs nav-tabs-pf margin-bottom-15">
                  <li :class="{ 'active': connectionHistoryInterval === 'today' }">
                    <a @click="showConnectionHistory(connectionHistoryAccount, 'today')">
                      {{ $t('openvpn_rw.today') }}
                    </a>
                  </li>
                  <li :class="{ 'active': connectionHistoryInterval === 'last_week' }">
                    <a @click="showConnectionHistory(connectionHistoryAccount, 'last_week')">
                      {{ $t('openvpn_rw.last_week') }}
                    </a>
                  </li>
                  <li :class="{ 'active': connectionHistoryInterval === 'last_month' }">
                    <a @click="showConnectionHistory(connectionHistoryAccount, 'last_month')">
                      {{ $t('openvpn_rw.last_month') }}
                    </a>
                  </li>
                </ul>
                <vue-good-table
                  :customRowsPerPageDropdown="[5,10,20]"
                  :perPage="5"
                  :columns="connectionHistoryColumns"
                  :rows="connectionHistory[connectionHistoryInterval][connectionHistoryAccount]"
                  :lineNumbers="false"
                  :defaultSortBy="{field: 'startTime', type: 'desc'}"
                  :globalSearch="false"
                  :paginate="true"
                  styleClass="table"
                  :nextText="tableLangsTexts.nextText"
                  :prevText="tableLangsTexts.prevText"
                  :rowsPerPageText="tableLangsTexts.rowsPerPageText"
                  :globalSearchPlaceholder="tableLangsTexts.globalSearchPlaceholder"
                  :ofText="tableLangsTexts.ofText"
                >
                  <template slot="table-row" slot-scope="props">
                    <td class="fancy">
                      {{ props.row.startTime | shortDateFormat }}
                    </td>
                    <td class="fancy">
                      {{ props.row.endTime | shortDateFormat }}
                    </td>
                    <td class="fancy">
                      {{ props.row.duration | secondsInHour }}
                    </td>
                    <td class="fancy">
                      {{ props.row.virtualIpAddress }}
                    </td>
                    <td class="fancy">
                      {{ props.row.remoteIpAddress }}
                    </td>
                    <td class="fancy">
                      {{ props.row.bytesReceived | byteFormat }}
                    </td>
                    <td class="fancy">
                      {{ props.row.bytesSent | byteFormat }}
                    </td>
                  </template>
                </vue-good-table>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('close')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- END MODALS -->
  </div>
</template>

<script>
export default {
  name: "OpenVPNRW",
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/feature/read"],
        {
          name: "openvpn"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }

          vm.view.menu = success;
        },
        function(error) {
          console.error(error);
        },
        false
      );
    });
  },
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  mounted() {
    this.getConfiguration();
    this.getInterfaces();
    this.getUsers();
    this.getCustoms();
  },
  data() {
    return {
      view: {
        isLoaded: false,
        menu: {
          installed: false,
          packages: []
        }
      },
      configuration: {
        status: "disabled"
      },
      newConfiguration: {
        isLoading: false,
        isEdit: false,
        advanced: false,
        Digest: "auto",
        Cipher: "auto",
        Remote: [],
        errors: this.initConfigurationErrors()
      },
      users: [],
      interfaces: [],
      accounts: [],
      ciphers: [],
      digests: [],
      toDownloadAccount: {
        name: ""
      },
      toSendEmailAccount: {
        address: ""
      },
      accountsColumns: [
        {
          label: this.$i18n.t("openvpn_rw.name"),
          field: "name",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_rw.user_mode"),
          field: "Mode",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_rw.certificate_expiration"),
          field: "Certificate",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_rw.reserved_ip"),
          field: "OpenVpnIp",
          filterable: true,
          sortFn: function(a, b, col, rowX, rowY) {
            a = a.split(".");
            b = b.split(".");
            for (var i = 0; i < a.length; i++) {
              if ((a[i] = parseInt(a[i])) < (b[i] = parseInt(b[i]))) return -1;
              else if (a[i] > b[i]) return 1;
            }
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.remote_network"),
          field: "VPNRemoteNetwork",
          filterable: true,
          sortFn: function(a, b, col, rowX, rowY) {
            a = a.split(".");
            b = b.split(".");
            for (var i = 0; i < a.length; i++) {
              if ((a[i] = parseInt(a[i])) < (b[i] = parseInt(b[i]))) return -1;
              else if (a[i] > b[i]) return 1;
            }
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.state"),
          field: "",
          filterable: true,
          sortable: true
        },
        {
          label: this.$i18n.t("openvpn_rw.last_connected"),
          field: "lastConnected",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        },
        {
          label: this.$i18n.t("action"),
          field: "",
          filterable: true,
          sortable: false
        }
      ],
      tableLangsTexts: this.tableLangs(),
      currentAccount: this.initAccount(),
      toDeleteAccount: {},
      toKillAccount: {},
      connectionHistoryAccount: '',
      connectionHistory: {
        today: [],
        last_week: [],
        last_month: []
      },
      connectionHistoryColumns: [
        {
          label: this.$i18n.t("openvpn_rw.started"),
          field: "startTime",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.ended"),
          field: "endTime",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.duration"),
          field: "duration",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.virtual_ip_address"),
          field: "virtualIpAddress",
          filterable: false
        },
        {
          label: this.$i18n.t("openvpn_rw.remote_ip_address"),
          field: "remoteIpAddress",
          filterable: false
        },
        {
          label: this.$i18n.t("openvpn_rw.bytes_received"),
          field: "bytesReceived",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        },
        {
          label: this.$i18n.t("openvpn_rw.bytes_sent"),
          field: "bytesSent",
          filterable: false,
          sortFn: function(a, b, col, rowX, rowY) {
            return (a < b ? -1 : (a > b ? 1 : 0));
          }
        }
      ],
      connectionHistoryInterval: 'today'
    };
  },
  methods: {
    installPackages() {
      this.view.isInstalling = true;
      // notification
      nethserver.notifications.success = this.$i18n.t("packages_installed_ok");
      nethserver.notifications.error = this.$i18n.t("packages_installed_error");

      nethserver.exec(
        ["nethserver-vpn/feature/update"],
        {
          name: "openvpn"
        },
        function(stream) {
          console.info("install-package", stream);
        },
        function(success) {
          // reload page
          window.parent.location.reload();
        },
        function(error) {
          console.error(error);
        }
      );
    },
    mapAuthMode(authMode) {
      switch (authMode) {
        case "password":
          return "username_password";

        case "certificate":
          return "certificate";

        case "password-certificate":
          return "username_password_certificate";
      }
    },
    initAccount() {
      return {
        name: "",
        OpenVpnIp: "",
        VPNRemoteNetmask: "",
        VPNRemoteNetwork: "",
        Mode: "vpn",
        advanced: false,
        errors: this.initAccountErrors()
      };
    },
    initAccountErrors() {
      return {
        name: {
          hasError: false,
          message: ""
        },
        OpenVpnIp: {
          hasError: false,
          message: ""
        },
        VPNRemoteNetmask: {
          hasError: false,
          message: ""
        },
        VPNRemoteNetwork: {
          hasError: false,
          message: ""
        },
        Mode: {
          hasError: false,
          message: ""
        }
      };
    },
    initConfigurationErrors() {
      return {
        AuthMode: {
          hasError: false,
          message: ""
        },
        BridgeEndIP: {
          hasError: false,
          message: ""
        },
        BridgeName: {
          hasError: false,
          message: ""
        },
        BridgeStartIP: {
          hasError: false,
          message: ""
        },
        Cipher: {
          hasError: false,
          message: ""
        },
        ClientToClient: {
          hasError: false,
          message: ""
        },
        Compression: {
          hasError: false,
          message: ""
        },
        Digest: {
          hasError: false,
          message: ""
        },
        Mode: {
          hasError: false,
          message: ""
        },
        Netmask: {
          hasError: false,
          message: ""
        },
        Network: {
          hasError: false,
          message: ""
        },
        PushDns: {
          hasError: false,
          message: ""
        },
        PushDomain: {
          hasError: false,
          message: ""
        },
        PushExtraRoutes: {
          hasError: false,
          message: ""
        },
        PushNbdd: {
          hasError: false,
          message: ""
        },
        PushWins: {
          hasError: false,
          message: ""
        },
        Remote: {
          hasError: false,
          message: ""
        },
        RouteToVPN: {
          hasError: false,
          message: ""
        },
        Port: {
          hasError: false,
          message: ""
        },
        Protocol: {
          hasError: false,
          message: ""
        },
        status: {
          hasError: false,
          message: ""
        },
        BridgeEndIP: {
          hasError: false,
          message: ""
        },
        BridgeName: {
          hasError: false,
          message: ""
        },
        BridgeStartIP: {
          hasError: false,
          message: ""
        },
        TlsVersionMin: {
          hasError: false,
          message: ""
        },
        CustomRoutes: {
          hasError: false,
          message: ""
        }
      };
    },
    getConfiguration() {
      var context = this;

      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "configuration"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.configuration = success.configuration;
          context.configuration.Remote = context.configuration.Remote.join(
            "\n"
          );
          context.configuration.CustomRoutes = context.configuration.CustomRoutes.join(
            "\n"
          );

          context.getAccounts();
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getAccounts() {
      var context = this;

      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "accounts"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.accounts = success.accounts;

          setTimeout(function() {
            $('[data-toggle="tooltip"]').tooltip();
          }, 750);
          context.view.isLoaded = true;
        },
        function(error) {
          console.error(error);
          context.view.isLoaded = true;
          context.accounts = [];
        }
      );
    },
    getInterfaces() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "interfaces"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.interfaces = success.interfaces;
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getUsers() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "users"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.users = success.users;
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getCustoms() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/read"],
        {
          action: "algorithms"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.ciphers = [
            { name: "auto", description: "auto_choose" }
          ].concat(
            success.algorithms.ciphers.sort((a, b) =>
              a.description > b.description
                ? 1
                : a.description === b.description
                ? a.name > b.name
                  ? 1
                  : -1
                : -1
            )
          );
          context.digests = [
            { name: "auto", description: "auto_choose" }
          ].concat(
            success.algorithms.digests.sort((a, b) =>
              a.description > b.description
                ? 1
                : a.description === b.description
                ? a.name > b.name
                  ? 1
                  : -1
                : -1
            )
          );
        },
        function(error) {
          console.error(error);
        }
      );
    },
    toggleAdvancedConfiguration() {
      this.newConfiguration.advanced = !this.newConfiguration.advanced;
      this.$forceUpdate();
    },
    toggleAdvancedAccount() {
      if (this.currentAccount.isEdit) {
        this.currentAccount.advanced = true;
      } else {
        this.currentAccount.advanced = !this.currentAccount.advanced;
      }
      this.$forceUpdate();
    },
    toggleStatus(isEdit) {
      var context = this;
      if (!isEdit) {
        context.configuration.status =
          context.configuration.status == "enabled" ? "disabled" : "enabled";
      }
      context.configuration.isEdit = isEdit;

      if (context.configuration.status == "enabled") {
        context.newConfiguration = JSON.parse(
          JSON.stringify(context.configuration)
        );
        context.newConfiguration.errors = context.initConfigurationErrors();
        context.newConfiguration.isLoading = false;
        context.newConfiguration.isEdit = false;
        context.newConfiguration.advanced = false;
        context.newConfiguration.Digest =
          context.newConfiguration.Digest == ""
            ? "auto"
            : context.newConfiguration.Digest;
        context.newConfiguration.Cipher =
          context.newConfiguration.Cipher == ""
            ? "auto"
            : context.newConfiguration.Cipher;
        $("#configureRWModal").modal("show");
      } else {
        // notification
        nethserver.notifications.success = context.$i18n.t(
          "openvpn_rw.configuration_updated_ok"
        );
        nethserver.notifications.error = context.$i18n.t(
          "openvpn_rw.configuration_updated_error"
        );

        // update values
        nethserver.exec(
          ["nethserver-vpn/openvpn-rw/update"],
          {
            status: "disabled",
            action: "configuration"
          },
          function(stream) {
            console.info("update-config", stream);
          },
          function(success) {
            // get all
            context.getConfiguration();
          },
          function(error, data) {
            console.error(error, data);
          }
        );
      }
    },
    resetConfiguration(isEdit) {
      if (this.configuration) {
        this.newConfiguration = this.configuration;
        this.newConfiguration.errors = this.initConfigurationErrors();
      }
    },
    saveConfiguration() {
      var context = this;

      var configObj = {
        status: this.newConfiguration.status,
        PushDomain: this.newConfiguration.PushDomain,
        PushExtraRoutes: this.newConfiguration.PushExtraRoutes,
        PushDns: this.newConfiguration.PushDns,
        PushWins: this.newConfiguration.PushWins,
        Digest: this.newConfiguration.Digest,
        Netmask:
          this.newConfiguration.Mode == "routed"
            ? this.newConfiguration.Netmask
            : null,
        Compression: this.newConfiguration.Compression,
        Mode: this.newConfiguration.Mode,
        Cipher: this.newConfiguration.Cipher,
        Port: this.newConfiguration.Port,
        PushNbdd: this.newConfiguration.PushNbdd,
        RouteToVPN: this.newConfiguration.RouteToVPN,
        Remote:
          this.newConfiguration.Remote.length > 0
            ? this.newConfiguration.Remote.split("\n")
            : [],
        Network:
          this.newConfiguration.Mode == "routed"
            ? this.newConfiguration.Network
            : null,
        BridgeStartIP:
          this.newConfiguration.Mode == "bridged"
            ? this.newConfiguration.BridgeStartIP
            : null,
        AuthMode: this.newConfiguration.AuthMode,
        BridgeName: this.newConfiguration.BridgeName,
        TlsVersionMin: this.newConfiguration.TlsVersionMin,
        ClientToClient: this.newConfiguration.ClientToClient,
        BridgeEndIP:
          this.newConfiguration.Mode == "bridged"
            ? this.newConfiguration.BridgeEndIP
            : null,
        Protocol: this.newConfiguration.Protocol,
        CustomRoutes:
          this.newConfiguration.CustomRoutes.length > 0
            ? this.newConfiguration.CustomRoutes.split("\n")
            : [],
        action: "configuration"
      };

      context.newConfiguration.isLoading = true;
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/validate"],
        configObj,
        null,
        function(success) {
          context.newConfiguration.isLoading = false;
          $("#configureRWModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "openvpn_rw.configuration_updated_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "openvpn_rw.configuration_updated_error"
          );

          // update values
          nethserver.exec(
            ["nethserver-vpn/openvpn-rw/update"],
            configObj,
            function(stream) {
              console.info("update-config", stream);
            },
            function(success) {
              // get all
              context.getConfiguration();
            },
            function(error, data) {
              console.error(error, data);
            }
          );
        },
        function(error, data) {
          var errorData = {};
          context.newConfiguration.isLoading = false;

          context.newConfiguration.errors = context.initConfigurationErrors();
          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.newConfiguration.errors[attr.parameter].hasError = true;
              context.newConfiguration.errors[attr.parameter].message =
                attr.error;
            }

            context.$forceUpdate();
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    openCreateAccount() {
      this.currentAccount = this.initAccount();

      $("#createAccountModal").modal("show");
    },
    openEditAccount(account) {
      this.currentAccount = JSON.parse(JSON.stringify(account));
      this.currentAccount.errors = this.initAccountErrors();

      this.currentAccount.isEdit = true;
      this.currentAccount.isLoading = false;
      this.currentAccount.advanced = true;
      $("#createAccountModal").modal("show");
    },
    saveAccount(account) {
      var context = this;

      var accountObj = {
        action: account.isEdit ? "update-account" : "create-account",
        type: context.currentAccount.Mode == "system" ? "vpn-user" : "vpn",
        name: context.currentAccount.name,
        OpenVpnIp: context.currentAccount.OpenVpnIp,
        VPNRemoteNetmask: context.currentAccount.VPNRemoteNetmask,
        VPNRemoteNetwork: context.currentAccount.VPNRemoteNetwork
      };

      context.currentAccount.isLoading = true;
      context.$forceUpdate();
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/validate"],
        accountObj,
        null,
        function(success) {
          context.currentAccount.isLoading = false;
          $("#createAccountModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "openvpn_rw.account_" +
              (context.currentAccount.isEdit ? "updated" : "created") +
              "_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "openvpn_rw.account_" +
              (context.currentAccount.isEdit ? "updated" : "created") +
              "_error"
          );

          // update values
          if (account.isEdit) {
            nethserver.exec(
              ["nethserver-vpn/openvpn-rw/update"],
              accountObj,
              function(stream) {
                console.info("account-edit", stream);
              },
              function(success) {
                // get all
                context.getAccounts();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          } else {
            nethserver.exec(
              ["nethserver-vpn/openvpn-rw/create"],
              accountObj,
              function(stream) {
                console.info("account-create", stream);
              },
              function(success) {
                // get all
                context.getAccounts();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          }
        },
        function(error, data) {
          var errorData = {};
          context.currentAccount.isLoading = false;
          context.currentAccount.errors = context.initAccountErrors();

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.currentAccount.errors[attr.parameter].hasError = true;
              context.currentAccount.errors[attr.parameter].message =
                attr.error;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    openDeleteAccount(account) {
      this.toDeleteAccount = JSON.parse(JSON.stringify(account));
      $("#deleteAccountModal").modal("show");
    },
    deleteAccount(account) {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_rw.account_deleted_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_rw.account_deleted_error"
      );

      $("#deleteAccountModal").modal("hide");
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/delete"],
        {
          name: account.name
        },
        function(stream) {
          console.info("account-delete", stream);
        },
        function(success) {
          // get all
          context.getAccounts();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    openKillAccount(account) {
      this.toKillAccount = JSON.parse(JSON.stringify(account));
      $("#killAccountModal").modal("show");
    },
    killAccount(account) {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_rw.account_killed_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_rw.account_killed_error"
      );

      $("#killAccountModal").modal("hide");
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/update"],
        {
          action: "kill",
          name: account.name
        },
        function(stream) {
          console.info("account-kill", stream);
        },
        function(success) {
          // get all
          context.getAccounts();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    toggleStatusAccount(account) {
      var context = this;
      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_rw.account_updated_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_rw.account_updated_error"
      );

      // update values
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/update"],
        {
          action: account.status == "enabled" ? "disable" : "enable",
          name: account.name
        },
        function(stream) {
          console.info("update-status", stream);
        },
        function(success) {
          // get all
          context.getAccounts();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    openDownloadAccount(account) {
      this.toDownloadAccount = JSON.parse(JSON.stringify(account));
      $("#downloadAccountModal").modal("show");
    },
    downloadAccount(name, type) {
      var extension = "";
      switch (type) {
        case "ovpn":
          extension = ".ovpn";
          break;
        case "pem":
          extension = ".pem";
          break;
        case "pkcs12":
          extension = ".p12";
          break;
      }

      // download actions
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "download",
          type: type,
          name: name
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          require("downloadjs")(atob(success.data), success.filename);
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    openSendEmailAccount(account) {
      this.toSendEmailAccount = JSON.parse(JSON.stringify(account));
      this.toSendEmailAccount.address =
        account.Mode == "system" ? account.name : "";
      $("#sendEmailAccountModal").modal("show");
    },
    sendEmailAccount() {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_rw.email_sent_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_rw.email_sent_error"
      );

      // send email action
      nethserver.exec(
        ["nethserver-vpn/openvpn-rw/read"],
        {
          action: "mail",
          name: this.toSendEmailAccount.name,
          address: this.toSendEmailAccount.address
        },
        function(stream) {
          console.log("send with mail", stream);
        },
        function(success) {
          $("#sendEmailAccountModal").modal("hide");
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    showStatistics(stats) {
      var html = "";

      html += "<dl>";
      html +=
        "<dt>" +
        this.$i18n.t("openvpn_rw.since") +
        "</dt><dd>" +
        stats.since +
        "</dd>";
      html +=
        "<dt>" +
        this.$i18n.t("openvpn_rw.virtual_address") +
        "</dt><dd>" +
        stats.virtual_address +
        "</dd>";
      html +=
        "<dt>" +
        this.$i18n.t("openvpn_rw.real_address") +
        "</dt><dd>" +
        stats.real_address +
        "</dd>";
      html +=
        "<dt>" +
        this.$i18n.t("openvpn_rw.bytes_sent") +
        "</dt><dd>" +
        this.$options.filters.byteFormat(stats.bytes_sent) +
        "</dd>";
      html +=
        "<dt>" +
        this.$i18n.t("openvpn_rw.bytes_received") +
        "</dt><dd>" +
        this.$options.filters.byteFormat(stats.bytes_received) +
        "</dd>";
      html += "</dl>";

      return html;
    },
    showConnectionHistory(accountName, timeInterval) {
      this.connectionHistoryAccount = accountName;
      this.connectionHistoryInterval = timeInterval;
      $("#connectionHistoryModal").modal("show");

      // retrieve connection history only once
      if (!this.connectionHistory[timeInterval][accountName]) {
        var context = this;
        nethserver.exec(
          ["nethserver-vpn/openvpn-rw/read"],
          {
            action: "connectionHistory",
            account: accountName,
            timeInterval: timeInterval
          },
          null,
          function(success) {
            try {
              success = JSON.parse(success);
              context.connectionHistory[timeInterval][accountName] = success.connectionHistory;
              context.$forceUpdate();
            } catch (e) {
              console.error(e);
            }
          },
          function(error) {
            console.error(error);
          }
        );
      }
    }
  }
};
</script>

<style scoped>
.span-left-margin {
  margin-left: 5px;
}
.proxy-details {
  margin-left: 10px;
}
.semi-bold {
  font-weight: 500;
}
.min-textarea-height {
  min-height: 100px;
}
.gray {
  color: #72767b;
}
.text-center {
  text-align: center;
}
.width-800 {
  width: 800px;
}
.margin-bottom-15 {
  margin-bottom: 15px;
}
</style>
