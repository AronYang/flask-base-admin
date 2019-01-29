<template>
  <router-link :to="url" class="nav-link">
    <div :style="{'padding-left':padding*20 + 'px'}">
    <i :class="icon"></i> 
    {{name}}
    <b-badge :variant="badge.variant">{{badge.text}}</b-badge>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'sidebar-nav-link',
  props: {
    name: {
      type: String,
      default: ''
    },
    url: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    },
    badge: {
      default: ''
    },
    padding: {
      type: Number,
      default: 1
    }
  }
}
</script>
