<template>
	<div class="board">
		<template v-for="(row, rowIndex) in tiles">
			<piece
				v-for="(tile, columnIndex) in row"
				:color="tile.color"
				:value="tile.value"
				:ownerColor="tile.owner_color"
				:resources="tile.resources"
				:kind="tile.name"
				:key="`${tile.name}_${columnIndex}_${rowIndex}`"
				:style="{ gridColumn: columnIndex + 1, gridRow: rowIndex + 1 }"
			>
			</piece>
		</template>
	</div>
</template>

<script>
const piece = require('./piece.vue');

module.exports = {
  props: ['tiles'],
  components: { piece },
};
</script>
