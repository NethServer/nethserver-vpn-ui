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
    <h2>{{ $t('ipsec.title') }}</h2>

    <div v-if="!view.isLoaded" class="spinner spinner-lg view-spinner"></div>
    <div v-show="view.isLoaded">
      <div v-if="tunnels.length == 0 && view.isLoaded" class="blank-slate-pf" id>
        <div class="blank-slate-pf-icon">
          <span class="pficon pficon-locked"></span>
        </div>
        <h1>{{$t('ipsec.no_tunnels_found')}}</h1>
        <p>{{$t('ipsec.no_tunnels_found_desc')}}.</p>
        <div class="blank-slate-pf-main-action">
          <button @click="openCreate()" class="btn btn-primary btn-lg">{{$t('ipsec.add_tunnel')}}</button>
        </div>
      </div>
      <div class="pf-container" v-if="tunnels.length > 0 && view.isLoaded">
        <h3>{{$t('actions')}}</h3>
        <button @click="openCreate()" class="btn btn-primary btn-lg">{{$t('ipsec.add_tunnel')}}</button>

        <h3>{{$t('list')}}</h3>
        <ul class="list-group list-view-pf list-view-pf-view no-mg-top mg-top-10">
          <li
            :class="[r.status == 'disabled' ? 'gray-list' : 'blue-list', 'list-group-item', r.status == 'disabled' ? 'gray' : '']"
            v-for="(r,k) in tunnels"
            v-bind:key="k"
          >
            <div class="list-view-pf-actions">
              <button
                @click="r.status == 'disabled' ? toggleStatus(r) : openEdit(r)"
                :class="['btn btn-default', r.status == 'disabled' ? 'btn-primary' : '']"
              >
                <span
                  :class="['fa', r.status == 'disabled' ? 'fa-check' : 'fa-pencil', 'span-right-margin']"
                ></span>
                {{r.status == 'disabled' ? $t('enable') : $t('edit')}}
              </button>
              <div class="dropdown pull-right dropdown-kebab-pf">
                <button
                  class="btn btn-link dropdown-toggle"
                  type="button"
                  id="dropdownKebabRight9"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="true"
                >
                  <span class="fa fa-ellipsis-v"></span>
                </button>
                <ul class="dropdown-menu dropdown-menu-right">
                  <li>
                    <a @click="toggleStatus(r)">
                      <span
                        :class="['fa', r.status == 'enabled' ? 'fa-lock' : 'fa-check', 'span-right-margin']"
                      ></span>
                      {{r.status == 'enabled' ? $t('disable') : $t('enable')}}
                    </a>
                  </li>
                  <li role="presentation" class="divider"></li>
                  <li>
                    <a @click="openDelete(r)">
                      <span class="fa fa-times span-right-margin"></span>
                      {{$t('delete')}}
                    </a>
                  </li>
                </ul>
              </div>
            </div>

            <div class="list-view-pf-main-info small-list">
              <div class="list-view-pf-left">
                <span :class="['pficon pficon-locked', 'list-view-pf-icon-sm']"></span>
              </div>
              <div class="list-view-pf-body">
                <div class="list-view-pf-description">
                  <div class="list-group-item-heading">{{r.name}}</div>
                  <div class="list-group-item-text">
                    <div class="inline-block">
                      <b>{{$t('ipsec.local_subnets')}}</b>
                      <br>
                      {{r.leftsubnets && r.leftsubnets.length > 0 && r.leftsubnets.join(',') || '-'}}
                    </div>
                    <span class="fa fa-arrow-right adjust-span-margin"></span>
                    <div class="inline-block">
                      <b>{{$t('ipsec.remote_subnets')}}</b>
                      <br>
                      {{r.rightsubnets && r.rightsubnets.length > 0 && r.rightsubnets.join(',') || '-'}}
                    </div>
                  </div>
                </div>
                <div class="list-view-pf-additional-info">
                  <div class="list-view-pf-additional-info-item">
                    <span :class="['fa', r.statistics ? 'fa-check green' : 'fa-times red']"></span>
                    {{r.statistics ? $t('ipsec.active') : $t('ipsec.not_active')}}
                  </div>
                  <div v-if="r.statistics" class="list-view-pf-additional-info-item">
                    <span class="fa fa-arrow-down"></span>
                    {{r.statistics.received_bytes | byteFormat}}
                    <span
                      class="gray"
                    >{{$t('ipsec.received')}}</span>
                  </div>
                  <div v-if="r.statistics" class="list-view-pf-additional-info-item">
                    <span class="fa fa-arrow-up"></span>
                    {{r.statistics.sent_bytes | byteFormat}} {{$t('ipsec.sent')}}
                  </div>
                  <div v-if="r.statistics" class="list-view-pf-additional-info-item">
                    <span class="fa fa-clock-o"></span>
                    {{r.statistics.started | dateFormat}} {{$t('ipsec.started')}}
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- MODALS -->
    <div class="modal" id="createTunnelModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
            >{{currentTunnel.isEdit ? $t('ipsec.edit_tunnel') + ' '+ currentTunnel.name : $t('ipsec.add_tunnel')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveTunnel(currentTunnel)">
            <div class="modal-body">
              <div :class="['form-group', currentTunnel.errors.name.hasError ? 'has-error' : '']">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.name')}}</label>
                <div class="col-sm-9">
                  <input :disabled="currentTunnel.isEdit" required type="text" v-model="currentTunnel.name" class="form-control">
                  <span
                    v-if="currentTunnel.errors.name.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.name.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span class="field-section-toggle-pf">{{$t('ipsec.connection')}}</span>
              </legend>

              <div
                :class="['form-group', currentTunnel.errors.left.hasError || currentTunnel.errors.right.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.left')}}</label>
                <div class="col-sm-4">
                  <select required v-model="currentTunnel.left" class="form-control">
                    <option
                      v-for="(i,ik) in interfaces"
                      :key="ik"
                      :value="i.name"
                    >{{i.name}} - {{i.address | uppercase}}</option>
                  </select>
                  <span
                    v-if="currentTunnel.errors.left.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.left.message)}}</span>
                </div>
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.right')}}</label>
                <div class="col-sm-4">
                  <input required type="text" v-model="currentTunnel.right" class="form-control">
                  <span
                    v-if="currentTunnel.errors.right.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.right.message)}}</span>
                </div>
              </div>
              <div
                :class="['form-group', currentTunnel.errors.leftsubnets.hasError || currentTunnel.errors.rightsubnets.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.leftsubnets')}}</label>
                <div class="col-sm-4">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnel.leftsubnets"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnel.errors.leftsubnets.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.leftsubnets.message)}}</span>
                </div>
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.rightsubnets')}}</label>
                <div class="col-sm-4">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnel.rightsubnets"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnel.errors.rightsubnets.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.rightsubnets.message)}}</span>
                </div>
              </div>
              <div
                :class="['form-group', currentTunnel.errors.leftid.hasError || currentTunnel.errors.rightid.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.leftid')}}</label>
                <div class="col-sm-4">
                  <input
                    :placeholder="'@'+currentTunnel.name+'.local'"
                    type="text"
                    v-model="currentTunnel.leftid"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnel.errors.leftid.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.leftid.message)}}</span>
                </div>
                <label
                  class="col-sm-2 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.rightid')}}</label>
                <div class="col-sm-4">
                  <input
                    :placeholder="'@'+currentTunnel.name+'.remote'"
                    type="text"
                    v-model="currentTunnel.rightid"
                    class="form-control"
                  >
                  <span
                    v-if="currentTunnel.errors.rightid.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.rightid.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span class="field-section-toggle-pf">{{$t('ipsec.authentication')}}</span>
              </legend>

              <div :class="['form-group', currentTunnel.errors.psk.hasError ? 'has-error' : '']">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.psk')}}</label>
                <div class="col-sm-9">
                  <textarea
                    required
                    type="text"
                    v-model="currentTunnel.psk"
                    class="form-control min-textarea-height"
                  ></textarea>
                  <span
                    v-if="currentTunnel.errors.psk.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.psk.message)}}</span>
                </div>
              </div>

              <legend class="fields-section-header-pf" aria-expanded="true">
                <span
                  :class="['fa fa-angle-right field-section-toggle-pf', currentTunnel.advanced ? 'fa-angle-down' : '']"
                ></span>
                <a
                  class="field-section-toggle-pf"
                  @click="toggleAdvancedMode()"
                >{{$t('advanced_mode')}}</a>
              </legend>

              <div
                v-show="currentTunnel.advanced"
                :class="['form-group', currentTunnel.errors.dpdaction.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.dpdaction')}}</label>
                <div class="col-sm-9">
                  <input type="checkbox" v-model="currentTunnel.dpdaction" class="form-control">
                  <span
                    v-if="currentTunnel.errors.dpdaction.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.dpdaction.message)}}</span>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced"
                :class="['form-group', currentTunnel.errors.pfs.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.pfs')}}</label>
                <div class="col-sm-9">
                  <input type="checkbox" v-model="currentTunnel.pfs" class="form-control">
                  <span
                    v-if="currentTunnel.errors.pfs.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.pfs.message)}}</span>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced"
                :class="['form-group', currentTunnel.errors.compress.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.compress')}}</label>
                <div class="col-sm-9">
                  <input type="checkbox" v-model="currentTunnel.compress" class="form-control">
                  <span
                    v-if="currentTunnel.errors.compress.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.compress.message)}}</span>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced"
                :class="['form-group', currentTunnel.errors.ike.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.ike')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnel.ike" class="form-control">
                    <option value="auto">{{$t('ipsec.auto')}}</option>
                    <option value="custom">{{$t('ipsec.custom')}}</option>
                  </select>
                  <span
                    v-if="currentTunnel.errors.ike.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.ike.message)}}</span>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.ike == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.cipher')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.ikecipher" class="form-control">
                    <option v-for="(i,ik) in ciphers" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.ike == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.hash')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.ikehash" class="form-control">
                    <option v-for="(i,ik) in hashes" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.ike == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.pfsgroup')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.ikepfsgroup" class="form-control">
                    <option v-for="(i,ik) in pfsgroups" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.ike == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.key_lifetime')}}</label>
                <div class="col-sm-7">
                  <input type="number" v-model="currentTunnel.ikelifetime" class="form-control">
                </div>
              </div>

              <div
                v-show="currentTunnel.advanced"
                :class="['form-group', currentTunnel.errors.esp.hasError ? 'has-error' : '']"
              >
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.esp')}}</label>
                <div class="col-sm-9">
                  <select v-model="currentTunnel.esp" class="form-control">
                    <option value="auto">{{$t('ipsec.auto')}}</option>
                    <option value="custom">{{$t('ipsec.custom')}}</option>
                  </select>
                  <span
                    v-if="currentTunnel.errors.esp.hasError"
                    class="help-block"
                  >{{$t('validation.validation_failed')}}: {{$t('validation.'+currentTunnel.errors.esp.message)}}</span>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.esp == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.cipher')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.espcipher" class="form-control">
                    <option v-for="(i,ik) in ciphers" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.esp == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.hash')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.esphash" class="form-control">
                    <option v-for="(i,ik) in hashes" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.esp == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.pfsgroup')}}</label>
                <div class="col-sm-7">
                  <select v-model="currentTunnel.esppfsgroup" class="form-control">
                    <option v-for="(i,ik) in pfsgroups" :key="ik" :value="i.name">{{i.description}}</option>
                  </select>
                </div>
              </div>
              <div
                v-show="currentTunnel.advanced && currentTunnel.esp == 'custom'"
                class="form-group"
              >
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >{{$t('ipsec.key_lifetime')}}</label>
                <div class="col-sm-7">
                  <input type="number" v-model="currentTunnel.salifetime" class="form-control">
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div v-if="currentTunnel.isLoading" class="spinner spinner-sm form-spinner-loader"></div>
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button
                class="btn btn-primary"
                type="submit"
              >{{currentTunnel.isEdit ? $t('edit') : $t('save')}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal" id="deleteTunnelModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{$t('ipsec.delete_tunnel')}} {{toDeleteTunnel.name}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="deleteTunnel(toDeleteTunnel)">
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
    <!-- END MODALS -->
  </div>
</template>

<script>
export default {
  name: "IPSec",
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  mounted() {
    this.getTunnels();
    this.getInterfaces();
    this.getSubnets();
    this.getCustoms();
  },
  data() {
    return {
      view: {
        isLoaded: false
      },
      tunnels: [],
      currentTunnel: this.initTunnel(),
      toDeleteTunnel: {
        name: ""
      },
      interfaces: [],
      subnets: [],
      ciphers: [],
      hashes: [],
      pfsgroups: []
    };
  },
  methods: {
    toggleAdvancedMode() {
      this.currentTunnel.advanced = !this.currentTunnel.advanced;
      this.$forceUpdate();
    },
    genPSK() {
      var a = new Uint8Array(32);
      window.crypto.getRandomValues(a);

      return btoa(String.fromCharCode.apply(null, a));
    },
    initTunnel() {
      return {
        psk: "",
        pfs: true,
        leftsubnets: [],
        left: "",
        esp: "auto",
        status: "enabled",
        name: "",
        rightid: "",
        leftid: "",
        dpdaction: false,
        right: "",
        compress: false,
        rightsubnets: [],
        ike: "auto",
        esphash: "md5",
        espcipher: "3des",
        esppfsgroup: "modp1024",
        salifetime: 3600,
        ikehash: "md5",
        ikecipher: "3des",
        ikepfsgroup: "modp1024",
        ikelifetime: 3600,
        statistics: null,
        errors: this.initErrors(),
        isEdit: false,
        isLoading: false,
        advanced: false
      };
    },
    initErrors() {
      return {
        name: {
          hasError: false,
          message: ""
        },
        left: {
          hasError: false,
          message: ""
        },
        right: {
          hasError: false,
          message: ""
        },
        leftsubnets: {
          hasError: false,
          message: ""
        },
        rightsubnets: {
          hasError: false,
          message: ""
        },
        leftid: {
          hasError: false,
          message: ""
        },
        rightid: {
          hasError: false,
          message: ""
        },
        psk: {
          hasError: false,
          message: ""
        },
        dpdaction: {
          hasError: false,
          message: ""
        },
        pfs: {
          hasError: false,
          message: ""
        },
        compress: {
          hasError: false,
          message: ""
        },
        ike: {
          hasError: false,
          message: ""
        },
        esp: {
          hasError: false,
          message: ""
        }
      };
    },
    getTunnels() {
      var context = this;

      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-vpn/ipsec/read"],
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
          context.tunnels = success.tunnels;
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
        ["nethserver-vpn/ipsec/read"],
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
    getSubnets() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/ipsec/read"],
        {
          action: "subnets"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.subnets = success.subnets;
        },
        function(error) {
          console.error(error);
        }
      );
    },
    getCustoms() {
      var context = this;

      nethserver.exec(
        ["nethserver-vpn/ipsec/read"],
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
          context.ciphers = success.algorithms.ciphers;
          context.hashes = success.algorithms.hashes;
          context.pfsgroups = success.algorithms.pfsgroups;
        },
        function(error) {
          console.error(error);
        }
      );
    },
    toggleStatus(tunnel) {
      var context = this;
      // notification
      nethserver.notifications.success = context.$i18n.t(
        "ipsec.tunnel_updated_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "ipsec.tunnel_updated_error"
      );

      // update values
      nethserver.exec(
        ["nethserver-vpn/ipsec/update"],
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
    openCreate() {
      this.currentTunnel = this.initTunnel();
      this.currentTunnel.psk = this.genPSK();
      this.currentTunnel.leftsubnets =
        this.subnets && this.subnets.length > 0 ? this.subnets.join("\n") : "";
      $("#createTunnelModal").modal("show");
    },
    openEdit(tunnel) {
      this.currentTunnel = JSON.parse(JSON.stringify(tunnel));
      this.currentTunnel.errors = this.initErrors();
      this.currentTunnel.leftsubnets = this.currentTunnel.leftsubnets.join(
        "\n"
      );
      this.currentTunnel.rightsubnets = this.currentTunnel.rightsubnets.join(
        "\n"
      );
      this.currentTunnel.isEdit = true;
      this.currentTunnel.isLoading = false;
      this.currentTunnel.advanced = false;
      $("#createTunnelModal").modal("show");
    },
    saveTunnel(tunnel) {
      var context = this;

      var tunnelObj = {
        action: tunnel.isEdit ? "update" : "create",

        name: context.currentTunnel.name,
        psk: context.currentTunnel.psk,

        left: context.currentTunnel.left,
        right: context.currentTunnel.right,
        leftsubnets:
          context.currentTunnel.leftsubnets.length > 0
            ? context.currentTunnel.leftsubnets.split("\n")
            : [],
        rightsubnets:
          context.currentTunnel.rightsubnets.length > 0
            ? context.currentTunnel.rightsubnets.split("\n")
            : [],
        rightid: context.currentTunnel.rightid,
        leftid: context.currentTunnel.leftid,

        esp: context.currentTunnel.esp,
        ike: context.currentTunnel.ike,

        esphash: context.currentTunnel.esphash,
        espcipher: context.currentTunnel.espcipher,
        esppfsgroup: context.currentTunnel.esppfsgroup,
        salifetime: context.currentTunnel.salifetime,
        ikehash: context.currentTunnel.ikehash,
        ikecipher: context.currentTunnel.ikecipher,
        ikepfsgroup: context.currentTunnel.ikepfsgroup,
        ikelifetime: context.currentTunnel.ikelifetime,

        status: "enabled",
        pfs: context.currentTunnel.pfs,
        dpdaction: context.currentTunnel.dpdaction,
        compress: context.currentTunnel.compress
      };

      context.currentTunnel.isLoading = true;
      context.$forceUpdate();
      nethserver.exec(
        ["nethserver-vpn/ipsec/validate"],
        tunnelObj,
        null,
        function(success) {
          context.currentTunnel.isLoading = false;
          $("#createTunnelModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "ipsec.tunnel_" +
              (context.currentTunnel.isEdit ? "updated" : "created") +
              "_ok"
          );
          nethserver.notifications.error = context.$i18n.t(
            "ipsec.tunnel_" +
              (context.currentTunnel.isEdit ? "updated" : "created") +
              "_error"
          );

          // update values
          if (tunnel.isEdit) {
            nethserver.exec(
              ["nethserver-vpn/ipsec/update"],
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
              ["nethserver-vpn/ipsec/create"],
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
          context.currentTunnel.isLoading = false;
          context.currentTunnel.errors = context.initErrors();

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.currentTunnel.errors[attr.parameter].hasError = true;
              context.currentTunnel.errors[attr.parameter].message = attr.error;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    openDelete(tunnel) {
      this.toDeleteTunnel = JSON.parse(JSON.stringify(tunnel));
      $("#deleteTunnelModal").modal("show");
    },
    deleteTunnel(tunnel) {
      var context = this;

      // notification
      nethserver.notifications.success = context.$i18n.t(
        "ipsec.tunnel_deleted_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "ipsec.tunnel_deleted_error"
      );

      $("#deleteTunnelModal").modal("hide");
      nethserver.exec(
        ["nethserver-vpn/ipsec/delete"],
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
</style>
