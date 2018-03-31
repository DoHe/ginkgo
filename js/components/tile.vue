<template>
	<div class="rect" :class="[colorClass]">
		{{ value }}<span v-if="resources !== undefined">/<span :class="[ownerColorClass]">{{ resources }}</span></span>
	</div>
</template>

<script>
module.exports = {
  props: ['color', 'value', 'ownerColor', 'resources'],
  computed: {
  	colorClass() { return `bg--${this.color}`; },
  	ownerColorClass() { return `ft--${this.owner_color || 'gray'}`; },
  },
};
</script>
