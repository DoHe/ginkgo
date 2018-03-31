<template>
	<div>
		<template v-if="kind === 'tile'">
			<tile
				:color="color"
				:value="value"
				:ownerColor="ownerColor"
				:resources="resources"
			>
			</tile>
		</template>
		<template v-else-if="kind === 'marker'">
			<markerPiece :value="value"></markerPiece>
		</template>
		<template v-else>
		</template>
	</div>
</template>

<script>
const tile = require('./tile.vue');
const markerPiece = require('./markerPiece.vue');

module.exports = {
  props: ['kind', 'color', 'value', 'ownerColor', 'resources'],
  components: { markerPiece, tile },
};
</script>
