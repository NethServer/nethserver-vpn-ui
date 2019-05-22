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
    <h2>{{ $t('openvpn_tun.title') }}</h2>

    <div v-if="!view.isLoaded" class="spinner spinner-lg view-spinner"></div>
    <div v-show="view.isLoaded">
      <ul class="nav nav-tabs nav-tabs-pf">
        <li>
          <a
            class="nav-link"
            data-toggle="tab"
            href="#servers-tab"
            id="servers-tab-parent"
          >{{$t('openvpn_tun.tun_servers')}}</a>
        </li>
        <li>
          <a
            class="nav-link"
            data-toggle="tab"
            href="#clients-tab"
            id="clients-tab-parent"
          >{{$t('openvpn_tun.tun_clients')}}</a>
        </li>
      </ul>

      <div class="tab-content" id="tunnelsTabContent">
        <div
          class="tab-pane fade active"
          id="servers-tab"
          role="tabpanel"
          aria-labelledby="servers-tab"
        >
          <div v-if="serverTunnels.length == 0 && view.isLoaded" class="blank-slate-pf" id>
            <div class="blank-slate-pf-icon">
              <span class="pficon pficon-locked"></span>
            </div>
            <h1>{{$t('openvpn_tun.no_tunnels_servers_found')}}</h1>
            <p>{{$t('openvpn_tun.no_tunnels_servers_found_desc')}}.</p>
            <div class="blank-slate-pf-main-action">
              <button
                @click="openCreateServer()"
                class="btn btn-primary btn-lg"
              >{{$t('openvpn_tun.add_server_tunnel')}}</button>
            </div>
          </div>
          <div class="pf-container" v-if="serverTunnels.length > 0 && view.isLoaded">
            <h3>{{$t('actions')}}</h3>
            <button
              @click="openCreateServer()"
              class="btn btn-primary btn-lg"
            >{{$t('openvpn_tun.add_server_tunnel')}}</button>

            <h3>{{$t('list')}}</h3>
            <vue-good-table
              v-show="view.isLoaded"
              :customRowsPerPageDropdown="[25,50,100]"
              :perPage="25"
              :columns="serverTunnelsColumns"
              :rows="serverTunnels"
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
                <td class="fancy">
                  <a @click="openEditServer(props.row)">
                    <strong>{{ props.row.name}}</strong>
                  </a>
                </td>
                <td class="fancy">{{props.row.Port}} ({{props.row.Protocol | uppercase}})</td>
                <td class="fancy">
                  <b>{{ props.row.Topology | uppercase}}</b>
                </td>
                <td class="fancy">{{ props.row.Network}}</td>
                <td class="fancy">
                  <div class="mg-top-view" v-for="(i,ik) in props.row.LocalNetworks" :key="ik">{{i}}</div>
                </td>
                <td class="fancy">
                  <div
                    class="mg-top-view"
                    v-for="(i,ik) in props.row.RemoteNetworks"
                    :key="ik"
                  >{{i}}</div>
                </td>
                <td class="fancy">
                  <span :class="['fa', props.row.running ? 'fa-check green' : 'fa-times red']"></span>
                </td>
                <td>
                  <button @click="openEditServer(props.row)" class="btn btn-default">
                    <span class="fa fa-pencil span-right-margin"></span>
                    {{$t('edit')}}
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
                        <a @click="openDownloadServer(props.row)">
                          <span class="fa fa-arrow-down span-right-margin"></span>
                          {{$t('download')}}
                        </a>
                      </li>
                      <li>
                        <a @click="toggleStatusServer(props.row)">
                          <span
                            :class="['fa', props.row.status == 'enabled' ? 'fa-lock' : 'fa-check', 'span-right-margin']"
                          ></span>
                          {{props.row.status == 'enabled' ? $t('disable') : $t('enable')}}
                        </a>
                      </li>
                      <li role="presentation" class="divider"></li>
                      <li>
                        <a @click="openDeleteServer(props.row)">
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
        </div>

        <div
          class="tab-pane fade active"
          id="clients-tab"
          role="tabpanel"
          aria-labelledby="clients-tab"
        >
          <div v-if="clientTunnels.length == 0 && view.isLoaded" class="blank-slate-pf" id>
            <div class="blank-slate-pf-icon">
              <span class="pficon pficon-locked"></span>
            </div>
            <h1>{{$t('openvpn_tun.no_tunnels_clients_found')}}</h1>
            <p>{{$t('openvpn_tun.no_tunnels_clients_found_desc')}}.</p>
            <div class="blank-slate-pf-main-action">
              <div class="btn-group">
                <button
                  @click="openCreateClient()"
                  class="btn btn-primary btn-lg shutdown-privileged"
                  data-action="restart"
                  data-container="body"
                >{{$t('openvpn_tun.add_client_tunnel')}}</button>
                <button
                  data-toggle="dropdown"
                  class="btn btn-primary btn-lg dropdown-toggle shutdown-privileged"
                >
                  <span class="caret"></span>
                </button>
                <ul role="menu" class="dropdown-menu">
                  <li class="presentation">
                    <a
                      @click="openUploadClient()"
                      role="menuitem"
                      data-action="restart"
                    >{{$t('openvpn_tun.upload_config')}}</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="pf-container" v-if="clientTunnels.length > 0 && view.isLoaded">
            <h3>{{$t('actions')}}</h3>
            <div class="btn-group">
              <button
                @click="openCreateClient()"
                class="btn btn-primary btn-lg shutdown-privileged"
                data-action="restart"
                data-container="body"
              >{{$t('openvpn_tun.add_client_tunnel')}}</button>
              <button
                data-toggle="dropdown"
                class="btn btn-primary btn-lg dropdown-toggle shutdown-privileged"
              >
                <span class="caret"></span>
              </button>
              <ul role="menu" class="dropdown-menu">
                <li class="presentation">
                  <a
                    @click="openUploadClient()"
                    role="menuitem"
                    data-action="restart"
                  >{{$t('openvpn_tun.upload_config')}}</a>
                </li>
              </ul>
            </div>

            <h3>{{$t('list')}}</h3>
            <vue-good-table
              v-show="view.isLoaded"
              :customRowsPerPageDropdown="[25,50,100]"
              :perPage="25"
              :columns="clientTunnelsColumns"
              :rows="clientTunnels"
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
                <td class="fancy">
                  <a @click="openEditClient(props.row)">
                    <strong>{{ props.row.name}}</strong>
                  </a>
                </td>
                <td class="fancy">{{props.row.RemotePort}}</td>
                <td class="fancy">
                  <b>{{ props.row.Topology | uppercase}}</b>
                </td>
                <td class="fancy">
                  <div class="mg-top-view" v-for="(i,ik) in props.row.RemoteHost" :key="ik">{{i}}</div>
                </td>
                <td class="fancy">
                  <span :class="['fa', props.row.running ? 'fa-check green' : 'fa-times red']"></span>
                </td>
                <td>
                  <button @click="openEditClient(props.row)" class="btn btn-default">
                    <span class="fa fa-pencil span-right-margin"></span>
                    {{$t('edit')}}
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
                        <a @click="toggleStatusClient(props.row)">
                          <span
                            :class="['fa', props.row.status == 'enabled' ? 'fa-lock' : 'fa-check', 'span-right-margin']"
                          ></span>
                          {{props.row.status == 'enabled' ? $t('disable') : $t('enable')}}
                        </a>
                      </li>
                      <li role="presentation" class="divider"></li>
                      <li>
                        <a @click="openDeleteClient(props.row)">
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
        </div>
      </div>
    </div>

    <!-- MODALS -->
    <div
      class="modal"
      id="createServerTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{currentTunnelServer.isEdit ? $t('openvpn_tun.edit_tunnel') + ' '+ currentTunnelServer.name : $t('openvpn_tun.add_tunnel')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveTunnelServer(currentTunnelServer)">
            <div class="modal-body">
              <div
                :class="['form-group', currentTunnelServer.errors.name.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.name')}}</label>
                <div class="col-sm-9">
                  <input
                    :disabled="currentTunnelServer.isEdit"
                    required
                    type="text"
                    v-model="currentTunnelServer.name"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelServer.errors.name.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.name.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span class="field-section-toggle-pf">{{$t('openvpn_tun.connection')}}</span>
              </legend>

              <div
                :class="['form-group', currentTunnelServer.errors.PublicAddresses.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.public_addresses')}}</label>
                <div class="col-sm-9">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnelServer.PublicAddresses"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelServer.errors.PublicAddresses.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.PublicAddresses.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', currentTunnelServer.errors.Port.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.port')}}</label>
                <div class="col-sm-9">
                  <input
                    required
                    type="number"
                    v-model="currentTunnelServer.Port"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelServer.errors.Port.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Port.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span class="field-section-toggle-pf">{{$t('openvpn_tun.routes')}}</span>
              </legend>

              <div
                :class="['form-group', currentTunnelServer.errors.LocalNetworks.hasError || currentTunnelServer.errors.RemoteNetworks.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.local_networks')}}</label>
                <div class="col-sm-4">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnelServer.LocalNetworks"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelServer.errors.LocalNetworks.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.LocalNetworks.message)}}</span>
                </div>
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_networks')}}</label>
                <div class="col-sm-4">
                  <textarea
                    type="text"
                    v-model="currentTunnelServer.RemoteNetworks"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelServer.errors.RemoteNetworks.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.RemoteNetworks.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', currentTunnelServer.errors.Topology.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.topology')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelServer.Topology" class="form-control">
                    <option value="subnet">{{$t('openvpn_tun.subnet')}}</option>
                    <option value="p2p">{{$t('openvpn_tun.p2p')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelServer.errors.Topology.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Topology.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelServer.Topology == 'subnet'"
                :class="['form-group', currentTunnelServer.errors.Network.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.vpn_network')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="currentTunnelServer.Network" class="form-control">
                  <span
                    v-if="currentTunnelServer.errors.Network.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Network.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelServer.Topology == 'p2p'"
                :class="['form-group', currentTunnelServer.errors.LocalPeer.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.local_p2p_ip')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="currentTunnelServer.LocalPeer" class="form-control">
                  <span
                    v-if="currentTunnelServer.errors.LocalPeer.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.LocalPeer.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelServer.Topology == 'p2p'"
                :class="['form-group', currentTunnelServer.errors.RemotePeer.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_p2p_ip')}}</label>
                <div class="col-sm-7">
                  <input type="text" v-model="currentTunnelServer.RemotePeer" class="form-control">
                  <span
                    v-if="currentTunnelServer.errors.RemotePeer.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.RemotePeer.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelServer.Topology == 'p2p'"
                :class="['form-group', currentTunnelServer.errors.Psk.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.psk')}}</label>
                <div class="col-sm-7">
                  <textarea
                    type="text"
                    v-model="currentTunnelServer.Psk"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelServer.errors.Psk.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Psk.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span
                  :class="['fa fa-angle-right field-section-toggle-pf', currentTunnelServer.advanced ? 'fa-angle-down' : '']"
                ></span>
                <a
                  class="field-section-toggle-pf"
                  @click="toggleAdvancedModeServer()"
                >{{$t('advanced_mode')}}</a>
              </legend>

              <div
                v-show="currentTunnelServer.advanced"
                :class="['form-group', currentTunnelServer.errors.Protocol.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.protocol')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelServer.Protocol" class="form-control">
                    <option value="udp">{{$t('openvpn_tun.udp')}}</option>
                    <option value="tcp">{{$t('openvpn_tun.tcp')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelServer.errors.Protocol.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Protocol.message)}}</span>
                </div>
              </div>

              <div
                v-show="currentTunnelServer.advanced"
                :class="['form-group', currentTunnelServer.errors.Compression.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.compress')}}</label>
                <div class="col-sm-9">
                  <input
                    type="checkbox"
                    v-model="currentTunnelServer.Compression"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelServer.errors.Compression.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelServer.errors.Compression.message)}}</span>
                </div>
              </div>

              <div v-show="currentTunnelServer.advanced" class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.digest')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelServer.Digest" class="form-control">
                    <option
                      v-for="(i,ik) in digests"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>
              <div v-show="currentTunnelServer.advanced" class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.cipher')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelServer.Cipher" class="form-control">
                    <option
                      v-for="(i,ik) in ciphers"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>
              <div v-show="currentTunnelServer.advanced" class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.tls_min_version')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelServer.TlsVersionMin" class="form-control">
                    <option value="auto">{{$t('openvpn_tun.auto')}}</option>
                    <option value="1.1">1.1</option>
                    <option value="1.2">1.2</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div
                v-if="currentTunnelServer.isLoading"
                class="spinner spinner-sm form-spinner-loader"
              ></div>
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button
                class="btn btn-primary"
                type="submit"
              >{{currentTunnelServer.isEdit ? $t('edit') : $t('save')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div
      class="modal"
      id="deleteServerTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{$t('openvpn_tun.delete_tunnel')}} {{toDeleteTunnelServer.name}}</h4>
          </div>
          <form
            class="form-horizontal"
            v-on:submit.prevent="deleteTunnelServer(toDeleteTunnelServer)"
          >
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

    <div
      class="modal"
      id="downloadServerTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{$t('openvpn_tun.download_configuration')}} {{toDownloadTunnelServer.name}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="undefined">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.tunnel_client_configuration')}}</label>
                <div class="col-sm-7 control-div" for="textInput-modal-markup">
                  <button
                    @click="downloadServer('client')"
                    class="btn btn-primary"
                  >{{$t('download')}}</button>
                </div>
              </div>

              <div class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.private_key_tun_ca')}}</label>
                <div class="col-sm-7 control-div" for="textInput-modal-markup">
                  <button @click="downloadServer('key')" class="btn btn-primary">{{$t('download')}}</button>
                </div>
              </div>

              <div class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.psk_download')}}</label>
                <div class="col-sm-7 control-div" for="textInput-modal-markup">
                  <button @click="downloadServer('psk')" class="btn btn-primary">{{$t('download')}}</button>
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
      id="createClientTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{currentTunnelClient.isEdit ? $t('openvpn_tun.edit_tunnel') + ' '+ currentTunnelClient.name : $t('openvpn_tun.add_tunnel')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveTunnelClient(currentTunnelClient)">
            <div class="modal-body">
              <div
                :class="['form-group', currentTunnelClient.errors.name.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.name')}}</label>
                <div class="col-sm-9">
                  <input
                    :disabled="currentTunnelClient.isEdit"
                    required
                    type="text"
                    v-model="currentTunnelClient.name"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.name.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.name.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span class="field-section-toggle-pf">{{$t('openvpn_tun.connection')}}</span>
              </legend>

              <div
                :class="['form-group', currentTunnelClient.errors.RemoteHost.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_hosts')}}</label>
                <div class="col-sm-9">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnelClient.RemoteHost"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelClient.errors.RemoteHost.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.RemoteHost.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', currentTunnelClient.errors.RemotePort.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_port')}}</label>
                <div class="col-sm-9">
                  <input
                    required
                    type="number"
                    v-model="currentTunnelClient.RemotePort"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.RemotePort.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.RemotePort.message)}}</span>
                </div>
              </div>

              <div
                :class="['form-group', currentTunnelClient.errors.Topology.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.topology')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelClient.Topology" class="form-control">
                    <option value="subnet">{{$t('openvpn_tun.subnet')}}</option>
                    <option value="p2p">{{$t('openvpn_tun.p2p')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelClient.errors.Topology.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Topology.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'subnet'"
                :class="['form-group', currentTunnelClient.errors.AuthMode.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.authentication')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnelClient.AuthMode" class="form-control">
                    <option value="certificate">{{$t('openvpn_tun.certificate')}}</option>
                    <option value="password-certificate">{{$t('openvpn_tun.password-certificate')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelClient.errors.AuthMode.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.AuthMode.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'subnet' && currentTunnelClient.AuthMode == 'certificate'"
                :class="['form-group', currentTunnelClient.errors.Certificate.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.certificate')}}</label>
                <div class="col-sm-7">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnelClient.Certificate"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelClient.errors.Certificate.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Certificate.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'subnet' && currentTunnelClient.AuthMode == 'password-certificate'"
                :class="['form-group', currentTunnelClient.errors.User.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.username')}}</label>
                <div class="col-sm-7">
                  <input
                    required
                    type="text"
                    v-model="currentTunnelClient.User"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.User.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.User.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'subnet' && currentTunnelClient.AuthMode == 'password-certificate'"
                :class="['form-group', currentTunnelClient.errors.Password.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.password')}}</label>
                <div class="col-sm-5">
                  <input
                    required
                    :type="currentTunnelClient.togglePass ? 'text' : 'password'"
                    v-model="currentTunnelClient.Password"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.Password.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Password.message)}}</span>
                </div>
                <div class="col-sm-2">
                  <button tabindex="-1" @click="togglePass()" type="button" class="btn btn-primary">
                    <span
                      :class="[!currentTunnelClient.togglePass ? 'fa fa-eye' : 'fa fa-eye-slash']"
                    ></span>
                  </button>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'subnet' && currentTunnelClient.AuthMode == 'password-certificate'"
                :class="['form-group', currentTunnelClient.errors.Certificate.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.certificate')}}</label>
                <div class="col-sm-7">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnelClient.Certificate"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelClient.errors.Certificate.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Certificate.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'p2p'"
                :class="['form-group', currentTunnelClient.errors.LocalPeer.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.local_p2p_ip')}}</label>
                <div class="col-sm-7">
                  <input
                    required
                    type="text"
                    v-model="currentTunnelClient.LocalPeer"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.LocalPeer.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.LocalPeer.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'p2p'"
                :class="['form-group', currentTunnelClient.errors.RemotePeer.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_p2p_ip')}}</label>
                <div class="col-sm-7">
                  <input
                    required
                    type="text"
                    v-model="currentTunnelClient.RemotePeer"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.RemotePeer.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.RemotePeer.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'p2p'"
                :class="['form-group', currentTunnelClient.errors.RemoteNetworks.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.remote_networks')}}</label>
                <div class="col-sm-7">
                  <textarea
                    type="text"
                    v-model="currentTunnelClient.RemoteNetworks"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelClient.errors.RemoteNetworks.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.RemoteNetworks.message)}}</span>
                </div>
              </div>

              <div
                v-if="currentTunnelClient.Topology == 'p2p'"
                :class="['form-group', currentTunnelClient.errors.Psk.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.psk')}}</label>
                <div class="col-sm-7">
                  <textarea
                    type="text"
                    v-model="currentTunnelClient.Psk"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnelClient.errors.Psk.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Psk.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span
                  :class="['fa fa-angle-right field-section-toggle-pf', currentTunnelClient.advanced ? 'fa-angle-down' : '']"
                ></span>
                <a
                  class="field-section-toggle-pf"
                  @click="toggleAdvancedModeClient()"
                >{{$t('advanced_mode')}}</a>
              </legend>

              <div
                v-show="currentTunnelClient.advanced"
                :class="['form-group', currentTunnelClient.errors.Mode.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.mode')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelClient.Mode" class="form-control">
                    <option value="bridged">{{$t('openvpn_tun.bridged')}}</option>
                    <option value="routed">{{$t('openvpn_tun.routed')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelClient.errors.Mode.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Mode.message)}}</span>
                </div>
              </div>

              <div
                v-show="currentTunnelClient.advanced"
                :class="['form-group', currentTunnelClient.errors.Protocol.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.protocol')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelClient.Protocol" class="form-control">
                    <option value="udp">{{$t('openvpn_tun.udp')}}</option>
                    <option value="tcp">{{$t('openvpn_tun.tcp')}}</option>
                  </select>
                  <span
                    v-if="currentTunnelClient.errors.Protocol.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Protocol.message)}}</span>
                </div>
              </div>

              <div
                v-show="currentTunnelClient.advanced"
                :class="['form-group', currentTunnelClient.errors.Compression.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.compress')}}</label>
                <div class="col-sm-9">
                  <input
                    type="checkbox"
                    v-model="currentTunnelClient.Compression"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.Compression.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.Compression.message)}}</span>
                </div>
              </div>

              <div v-show="currentTunnelClient.advanced" class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.digest')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelClient.Digest" class="form-control">
                    <option
                      v-for="(i,ik) in digests"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>
              <div v-show="currentTunnelClient.advanced" class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.cipher')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnelClient.Cipher" class="form-control">
                    <option
                      v-for="(i,ik) in ciphers"
                      :key="ik"
                      :value="i.name"
                    >{{i.name | uppercase}} ({{$t('openvpn_tun.'+i.description)}})</option>
                  </select>
                </div>
              </div>

              <div
                v-show="currentTunnelClient.advanced"
                :class="['form-group', currentTunnelClient.errors.WanPriorities.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.wan_priorities')}}</label>
                <div class="col-sm-9">
                  <input
                    required
                    type="checkbox"
                    v-model="currentTunnelClient.WanPriorities"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnelClient.errors.WanPriorities.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.WanPriorities.message)}}</span>
                </div>
              </div>

              <div
                v-show="currentTunnelClient.advanced && currentTunnelClient.WanPriorities"
                :class="['form-group', currentTunnelClient.errors.WanPrioritiesIFace.hasError ? 'has-error' : '']"
                v-for="(int,intk) in interfaces"
                :key="intk"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.wan_priorities_iface')}} {{intk+1}}</label>
                <div class="col-sm-7">
                  <select
                    v-model="currentTunnelClient.WanPrioritiesIFace[intk]"
                    class="form-control"
                  >
                    <option
                      v-for="(i,ik) in interfaces"
                      :key="ik"
                      :value="i.name"
                    >{{i.name}} - {{i.address | uppercase}}</option>
                  </select>
                  <span
                    v-if="currentTunnelClient.errors.WanPrioritiesIFace.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnelClient.errors.WanPrioritiesIFace.message)}}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div
                v-if="currentTunnelClient.isLoading"
                class="spinner spinner-sm form-spinner-loader"
              ></div>
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button
                class="btn btn-primary"
                type="submit"
              >{{currentTunnelClient.isEdit ? $t('edit') : $t('save')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div
      class="modal"
      id="deleteClientTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{$t('openvpn_tun.delete_tunnel')}} {{toDeleteTunnelClient.name}}</h4>
          </div>
          <form
            class="form-horizontal"
            v-on:submit.prevent="deleteTunnelClient(toDeleteTunnelClient)"
          >
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
    <div
      class="modal"
      id="uploadClientTunnelModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('openvpn_tun.upload_config')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="uploadClient()">
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('openvpn_tun.client_configuration')}}</label>
                <div class="col-sm-7">
                  <label for="config-upload-tun" class="custom-config-upload">
                    <i class="fa fa-cloud-upload span-right-margin"></i>
                    {{$t('openvpn_tun.choose_file')}}
                  </label>
                  <input
                    class="inputfile"
                    required
                    @change="onChangeInput($event)"
                    id="config-file"
                    name="config-upload-tun"
                    type="file"
                  >
                  <span
                    v-if="toUploadTunnelClient.errors.file.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+toUploadTunnelClient.errors.file.message)}}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div
                v-if="toUploadTunnelClient.isLoading"
                class="spinner spinner-sm form-spinner-loader"
              ></div>
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button class="btn btn-primary" type="submit">{{$t('upload')}}</button>
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
  name: "OpenVPNTun",
  mounted() {
    this.getTunnels();
    this.getInterfaces();
    this.getDefaults();
    this.getCustoms();
    $("#servers-tab-parent").click();
  },
  data() {
    return {
      view: {
        isLoaded: true
      },
      serverTunnels: [],
      serverTunnelsColumns: [
        {
          label: this.$i18n.t("openvpn_tun.name"),
          field: "name",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.port"),
          field: "Port",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.topology"),
          field: "Topology",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.vpn_network"),
          field: "Network",
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
          label: this.$i18n.t("openvpn_tun.local_networks"),
          field: "LocalNetworks",
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
          label: this.$i18n.t("openvpn_tun.remote_networks"),
          field: "RemoteNetworks",
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
          label: this.$i18n.t("openvpn_tun.state"),
          field: "status",
          filterable: true
        },
        {
          label: this.$i18n.t("action"),
          field: "",
          filterable: true,
          sortable: false
        }
      ],
      clientTunnels: [],
      clientTunnelsColumns: [
        {
          label: this.$i18n.t("openvpn_tun.name"),
          field: "name",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.remote_port"),
          field: "RemotePort",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.topology"),
          field: "Topology",
          filterable: true
        },
        {
          label: this.$i18n.t("openvpn_tun.remote_hosts"),
          field: "RemoteHost",
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
          label: this.$i18n.t("openvpn_tun.state"),
          field: "status",
          filterable: true
        },
        {
          label: this.$i18n.t("action"),
          field: "",
          filterable: true,
          sortable: false
        }
      ],
      currentTunnelServer: this.initTunnelServer(),
      toDeleteTunnelServer: {
        name: ""
      },
      toDownloadTunnelServer: {
        name: ""
      },
      currentTunnelClient: this.initTunnelClient(),
      toDeleteTunnelClient: {
        name: ""
      },
      toUploadTunnelClient: {
        file: "",
        isLoading: false,
        errors: {
          file: {
            hasError: false,
            message: ""
          }
        }
      },
      interfaces: [],
      defaults: {},
      ciphers: [],
      digests: [],
      tlss: [],
      tableLangsTexts: this.tableLangs()
    };
  },
  methods: {
    toggleAdvancedModeServer() {
      this.currentTunnelServer.advanced = !this.currentTunnelServer.advanced;
      this.$forceUpdate();
    },
    toggleAdvancedModeClient() {
      this.currentTunnelClient.advanced = !this.currentTunnelClient.advanced;
      this.$forceUpdate();
    },
    togglePass() {
      this.currentTunnelClient.togglePass = !this.currentTunnelClient
        .togglePass;
      this.$forceUpdate();
    },
    genPSK() {
      var a = new Uint8Array(32);
      window.crypto.getRandomValues(a);

      return btoa(String.fromCharCode.apply(null, a));
    },
    initTunnelServer() {
      return {
        name: "",
        Cipher: "auto",
        Compression: false,
        Digest: "auto",
        Network: "",
        Port: null,
        Protocol: "udp",
        PublicAddresses: [],
        LocalNetworks: [],
        RemoteNetworks: [],
        TlsVersionMin: "auto",
        Topology: "subnet",
        Psk: "",
        LocalPeer: "",
        RemotePeer: "",
        status: "enabled",
        errors: this.initErrorsServer(),
        isEdit: false,
        isLoading: false,
        advanced: false
      };
    },
    initErrorsServer() {
      return {
        name: {
          hasError: false,
          message: ""
        },
        PublicAddresses: {
          hasError: false,
          message: ""
        },
        Port: {
          hasError: false,
          message: ""
        },
        Network: {
          hasError: false,
          message: ""
        },
        Topology: {
          hasError: false,
          message: ""
        },
        LocalNetworks: {
          hasError: false,
          message: ""
        },
        RemoteNetworks: {
          hasError: false,
          message: ""
        },
        LocalPeer: {
          hasError: false,
          message: ""
        },
        RemotePeer: {
          hasError: false,
          message: ""
        },
        Psk: {
          hasError: false,
          message: ""
        },
        Protocol: {
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
        Cipher: {
          hasError: false,
          message: ""
        },
        TlsVersionMin: {
          hasError: false,
          message: ""
        }
      };
    },
    initTunnelClient() {
      return {
        name: "",
        AuthMode: "certificate",
        Cipher: "auto",
        Compression: false,
        Digest: "auto",
        Mode: "bridged",
        Password: "",
        togglePass: false,
        Protocol: "udp",
        RemoteHost: [],
        RemoteNetworks: [],
        LocalPeer: "",
        RemotePeer: "",
        RemotePort: null,
        Topology: "subnet",
        User: "",
        WanPriorities: false,
        WanPrioritiesIFace: [],
        Certificate: "",
        Psk: "",
        status: "enabled",
        errors: this.initErrorsClient(),
        isEdit: false,
        isLoading: false,
        advanced: false
      };
    },
    initErrorsClient() {
      return {
        name: {
          hasError: false,
          message: ""
        },
        AuthMode: {
          hasError: false,
          message: ""
        },
        Cipher: {
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
        Password: {
          hasError: false,
          message: ""
        },
        Protocol: {
          hasError: false,
          message: ""
        },
        RemoteHost: {
          hasError: false,
          message: ""
        },
        RemoteNetworks: {
          hasError: false,
          message: ""
        },
        LocalPeer: {
          hasError: false,
          message: ""
        },
        RemotePeer: {
          hasError: false,
          message: ""
        },
        RemotePort: {
          hasError: false,
          message: ""
        },
        Topology: {
          hasError: false,
          message: ""
        },
        User: {
          hasError: false,
          message: ""
        },
        WanPriorities: {
          hasError: false,
          message: ""
        },
        WanPrioritiesIFace: {
          hasError: false,
          message: ""
        },
        Certificate: {
          hasError: false,
          message: ""
        },
        Psk: {
          hasError: false,
          message: ""
        }
      };
    },
    getTunnels() {
      var context = this;

      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/read"],
        {
          action: "tunnels"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.serverTunnels = success.tunnels.filter(function(t) {
            return t.type == "openvpn-tunnel-server";
          });
          context.clientTunnels = success.tunnels.filter(function(t) {
            t.WanPrioritiesIFace = [];
            return t.type == "tunnel";
          });
          context.view.isLoaded = true;
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getInterfaces() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/read"],
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
    getDefaults() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/read"],
        {
          action: "server-defaults"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.defaults = success;
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
    toggleStatusServer(tunnel) {
      var context = this;
      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_tun.tunnel_updated_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_tun.tunnel_updated_error"
      );

      // update values
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/update"],
        {
          action: tunnel.status == "enabled" ? "disable" : "enable",
          name: tunnel.name
        },
        function(stream) {
          console.info("update-status", stream);
        },
        function(success) {
          // get all
          context.getTunnels();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    toggleStatusClient(tunnel) {
      var context = this;
      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_tun.tunnel_updated_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_tun.tunnel_updated_error"
      );

      // update values
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/update"],
        {
          action: tunnel.status == "enabled" ? "disable" : "enable",
          name: tunnel.name
        },
        function(stream) {
          console.info("update-status", stream);
        },
        function(success) {
          // get all
          context.getTunnels();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    openCreateServer() {
      this.currentTunnelServer = this.initTunnelServer();
      this.currentTunnelServer.Psk = this.defaults.Psk;
      this.currentTunnelServer.Network = this.defaults.Network;
      this.currentTunnelServer.Port = this.defaults.Port;
      this.currentTunnelServer.PublicAddresses = this.defaults.PublicAddresses;
      this.currentTunnelServer.LocalPeer = this.defaults.LocalPeer;
      this.currentTunnelServer.RemotePeer = this.defaults.RemotePeer;
      this.currentTunnelServer.LocalNetworks = this.defaults.LocalNetworks;

      $("#createServerTunnelModal").modal("show");
    },
    openCreateClient() {
      this.currentTunnelClient = this.initTunnelClient();
      this.currentTunnelClient.Psk = "";

      $("#createClientTunnelModal").modal("show");
    },
    openEditServer(tunnel) {
      this.currentTunnelServer = JSON.parse(JSON.stringify(tunnel));
      this.currentTunnelServer.errors = this.initErrorsServer();
      this.currentTunnelServer.PublicAddresses =
        this.currentTunnelServer.PublicAddresses.length > 0
          ? this.currentTunnelServer.PublicAddresses.join("\n")
          : [];
      this.currentTunnelServer.LocalNetworks =
        this.currentTunnelServer.LocalNetworks.length > 0
          ? this.currentTunnelServer.LocalNetworks.join("\n")
          : [];
      this.currentTunnelServer.RemoteNetworks =
        this.currentTunnelServer.RemoteNetworks.length > 0
          ? this.currentTunnelServer.RemoteNetworks.join("\n")
          : [];
      this.currentTunnelServer.isEdit = true;
      this.currentTunnelServer.isLoading = false;
      this.currentTunnelServer.advanced = false;
      $("#createServerTunnelModal").modal("show");
    },
    openEditClient(tunnel) {
      this.currentTunnelClient = JSON.parse(JSON.stringify(tunnel));
      this.currentTunnelClient.errors = this.initErrorsClient();
      this.currentTunnelClient.RemoteHost =
        this.currentTunnelClient.RemoteHost.length > 0
          ? this.currentTunnelClient.RemoteHost.join("\n")
          : [];
      this.currentTunnelClient.RemoteNetworks =
        this.currentTunnelClient.RemoteNetworks.length > 0
          ? this.currentTunnelClient.RemoteNetworks.join("\n")
          : [];
      this.currentTunnelClient.WanPriorities =
        this.currentTunnelClient.WanPriorities.length > 0;
      this.currentTunnelClient.WanPrioritiesIFace =
        this.currentTunnelClient.WanPriorities.length > 0
          ? this.currentTunnelClient.WanPriorities.split(",")
          : [];
      this.currentTunnelClient.togglePass = false;
      this.currentTunnelClient.isEdit = true;
      this.currentTunnelClient.isLoading = false;
      this.currentTunnelClient.advanced = false;
      $("#createClientTunnelModal").modal("show");
    },
    saveTunnelServer(tunnel) {
      var context = this;

      var tunnelObj = {
        action: tunnel.isEdit ? "update" : "create",

        name: context.currentTunnelServer.name,
        Psk: context.currentTunnelServer.Psk,

        left: context.currentTunnelServer.left,
        right: context.currentTunnelServer.right,
        rightid: context.currentTunnelServer.rightid,
        leftid: context.currentTunnelServer.leftid,

        esp: context.currentTunnelServer.esp,
        ike: context.currentTunnelServer.ike,

        esphash: context.currentTunnelServer.esphash,
        espcipher: context.currentTunnelServer.espcipher,
        esppfsgroup: context.currentTunnelServer.esppfsgroup,
        salifetime: context.currentTunnelServer.salifetime,
        ikehash: context.currentTunnelServer.ikehash,
        ikecipher: context.currentTunnelServer.ikecipher,
        ikepfsgroup: context.currentTunnelServer.ikepfsgroup,
        ikelifetime: context.currentTunnelServer.ikelifetime,

        status: "enabled",
        pfs: context.currentTunnelServer.pfs,
        dpdaction: context.currentTunnelServer.dpdaction,
        compress: context.currentTunnelServer.compress
      };

      context.currentTunnelServer.isLoading = true;
      context.$forceUpdate();
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/validate"],
        tunnelObj,
        null,
        function(success) {
          context.currentTunnelServer.isLoading = false;
          $("#createServerTunnelModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "openvpn_tun.tunnel_" +
              (context.currentTunnelServer.isEdit ? "updated" : "created") +
              "_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "openvpn_tun.tunnel_" +
              (context.currentTunnelServer.isEdit ? "updated" : "created") +
              "_error"
          );

          // update values
          if (tunnel.isEdit) {
            nethserver.exec(
              ["nethserver-vpn/openvpn-tunnel/update"],
              tunnelObj,
              function(stream) {
                console.info("tunnel-edit", stream);
              },
              function(success) {
                // get all
                context.getTunnels();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          } else {
            nethserver.exec(
              ["nethserver-vpn/openvpn-tunnel/create"],
              tunnelObj,
              function(stream) {
                console.info("tunnel-create", stream);
              },
              function(success) {
                // get all
                context.getTunnels();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          }
        },
        function(error, data) {
          var errorData = {};
          context.currentTunnelServer.isLoading = false;
          context.currentTunnelServer.errors = context.initErrorsServer();

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.currentTunnelServer.errors[
                attr.parameter
              ].hasError = true;
              context.currentTunnelServer.errors[attr.parameter].message =
                attr.error;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    saveTunnelClient(tunnel) {
      var context = this;

      console.log(context.currentTunnelClient);

      var tunnelObj = {
        action: tunnel.isEdit ? "update" : "create",

        name: context.currentTunnelClient.name,
        Psk: context.currentTunnelClient.Psk,

        left: context.currentTunnelClient.left,
        right: context.currentTunnelClient.right,
        rightid: context.currentTunnelClient.rightid,
        leftid: context.currentTunnelClient.leftid,

        esp: context.currentTunnelClient.esp,
        ike: context.currentTunnelClient.ike,

        esphash: context.currentTunnelClient.esphash,
        espcipher: context.currentTunnelClient.espcipher,
        esppfsgroup: context.currentTunnelClient.esppfsgroup,
        salifetime: context.currentTunnelClient.salifetime,
        ikehash: context.currentTunnelClient.ikehash,
        ikecipher: context.currentTunnelClient.ikecipher,
        ikepfsgroup: context.currentTunnelClient.ikepfsgroup,
        ikelifetime: context.currentTunnelClient.ikelifetime,

        status: "enabled",
        pfs: context.currentTunnelClient.pfs,
        dpdaction: context.currentTunnelClient.dpdaction,
        compress: context.currentTunnelClient.compress
      };

      context.currentTunnelClient.isLoading = true;
      context.$forceUpdate();
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/validate"],
        tunnelObj,
        null,
        function(success) {
          context.currentTunnelClient.isLoading = false;
          $("#createClientTunnelModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "openvpn_tun.tunnel_" +
              (context.currentTunnelClient.isEdit ? "updated" : "created") +
              "_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "openvpn_tun.tunnel_" +
              (context.currentTunnelClient.isEdit ? "updated" : "created") +
              "_error"
          );

          // update values
          if (tunnel.isEdit) {
            nethserver.exec(
              ["nethserver-vpn/openvpn-tunnel/update"],
              tunnelObj,
              function(stream) {
                console.info("tunnel-edit", stream);
              },
              function(success) {
                // get all
                context.getTunnels();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          } else {
            nethserver.exec(
              ["nethserver-vpn/openvpn-tunnel/create"],
              tunnelObj,
              function(stream) {
                console.info("tunnel-create", stream);
              },
              function(success) {
                // get all
                context.getTunnels();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
          }
        },
        function(error, data) {
          var errorData = {};
          context.currentTunnelClient.isLoading = false;
          context.currentTunnelClient.errors = context.initErrorsClient();

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.currentTunnelClient.errors[
                attr.parameter
              ].hasError = true;
              context.currentTunnelClient.errors[attr.parameter].message =
                attr.error;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    openDeleteServer(tunnel) {
      this.toDeleteTunnelServer = JSON.parse(JSON.stringify(tunnel));
      $("#deleteServerTunnelModal").modal("show");
    },
    openDeleteClient(tunnel) {
      this.toDeleteTunnelClient = JSON.parse(JSON.stringify(tunnel));
      $("#deleteClientTunnelModal").modal("show");
    },
    deleteTunnelServer(tunnel) {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_tun.tunnel_deleted_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_tun.tunnel_deleted_error"
      );

      $("#deleteServerTunnelModal").modal("hide");
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/delete"],
        {
          name: tunnel.name
        },
        function(stream) {
          console.info("tunnel-delete", stream);
        },
        function(success) {
          // get all
          context.getTunnels();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    deleteTunnelClient(tunnel) {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "openvpn_tun.tunnel_deleted_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "openvpn_tun.tunnel_deleted_error"
      );

      $("#deleteClientTunnelModal").modal("hide");
      nethserver.exec(
        ["nethserver-vpn/openvpn-tunnel/delete"],
        {
          name: tunnel.name
        },
        function(stream) {
          console.info("tunnel-delete", stream);
        },
        function(success) {
          // get all
          context.getTunnels();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    },
    openDownloadServer(tunnel) {
      this.toDownloadTunnelServer = JSON.parse(JSON.stringify(tunnel));
      $("#downloadServerTunnelModal").modal("show");
    },
    downloadServer(action) {
      switch (action) {
        case "client":
          break;

        case "key":
          break;

        case "psk":
          break;
      }
    },
    openUploadClient() {
      this.toUploadTunnelClient.file = "";
      this.toUploadTunnelClient.isLoading = false;
      $("#config-file").val("");
      $("#uploadClientTunnelModal").modal("show");
    },
    onChangeInput(event) {
      var context = this;
      this.getBase64(event.target.files[0], function(resp) {
        context.toUploadTunnelClient.file = resp;
        context.$forceUpdate();
      });
    },
    uploadClient() {
      var context = this;

      var configUp = {
        action: "upload-client",
        file: context.toUploadTunnelClient.file
      };

      context.toUploadTunnelClient.errors.isLoading = true;
      context.exec(
        ["nethserver-vpn/openvpn-tunnel/validate"],
        configUp,
        null,
        function(success) {
          context.toUploadTunnelClient.errors.isLoading = false;
          $("#uploadClientTunnelModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "openvpn_tun.tunnel_config_uploaded_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "openvpn_tun.tunnel_config_uploaded_error"
          );

          // upload config
          context.exec(
            ["nethserver-vpn/openvpn-tunnel/update"],
            configUp,
            function(stream) {
              console.info("upload-tunnel", stream);
            },
            function(success) {
              // get tunnels
              context.getTunnels();
            },
            function(error, data) {
              console.error(error, data);
            }
          );
        },
        function(error, data) {
          var errorData = {};
          context.toUploadTunnelClient.errors.isLoading = false;
          context.toUploadTunnelClient.errors.file.hasError = false;

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.toUploadTunnelClient.errors[
                attr.parameter
              ].hasError = true;
              context.toUploadTunnelClient.errors[attr.parameter].message =
                attr.error;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    }
  }
};
</script>

<style>
.min-textarea-height {
  min-height: 100px;
}

.gray-list {
  border-left: 3px solid #72767b !important;
}
.blue-list {
  border-left: 3px solid #0088ce !important;
}
.small-list {
  padding-top: 5px;
  padding-bottom: 5px;
}
.adjust-span-margin {
  margin-left: 15px;
  margin-right: 15px;
}

.red {
  color: #cc0000;
}
.green {
  color: #3f9c35;
}
.gray {
  color: #72767b;
}

.inline-block {
  display: inline-block;
}

.mg-top-view {
  margin-top: -10px;
}
</style>
