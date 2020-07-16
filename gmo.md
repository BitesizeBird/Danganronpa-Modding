# GMO format
Stores 3D model data. It appears to be a modified form of the PSP GMO format, which is documented [here][http://web.archive.org/web/20090922200620/http://www.richwhitehouse.com/index.php?postid=34].

## Header

| Offset | Size | Content |
| ------ | ---- | ------- |
| `0x00` | 16   | Magic string `OMG.00.1PSP` padded with 5 trailing zeroes |

A top-level entry (type `0x0002`) follows.

## Entries

This format is comprised of various _entries_, which can be nested. Each entry begins with the following metadata:

| Offset | Size | Content |
| ------ | ---- | ------- |
| `0x00` | 2 | Entry type |
| `0x02` | 2 | Entry header size |
| `0x04` | 4 | Entry total size (includes metadata) |

**Note:** in some cases, the header size is 0. This means there's no additional header data, and the actual data section begins at the offset `0x08`, right after the metadata.

### Top-level entry

Has a type of `0x0002`. This entry only appears once at the top level of each GMO file, and contails all others.

### Subentry

Has a type of `0x0003`, and is a child of the top-level entry.


### Model surface entry

Has a type of `0x0005`, and is a child of a subentry. This entry defines material, vertex and mesh data.

#### Mesh

Has a type of `0x0006`, and is a child of a model surface entry. This entry defines a mesh by referencing a vertex array with the same parent entry.

#### Vertex array

Has a type of `0x0007`, and is a child of a model surface entry. This entry defines an array of vertex data, which includes UVs and normal vectors.

| Offset | Size | Content |
| ------ | ---- | ------- |
| `0x00` | 4 | ??? |
| `0x04` | 4 | Vertex count |

The previous data is followed by 8 32-bit floating point values for each vertex:
* U coordinate
* V coordinate
* Normal vector X coordinate
* Normal vector Y coordinate
* Normal vector Z coordinate
* X coordinate
* Y coordinate
* Z coordinate
