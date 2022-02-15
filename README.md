# Dynamic Node Groups
Python addon to generate node groups dynamically

## Node Structs
Pseudo-struct types for passing around collections of values in a single socket. This is similar to combining float values in a vector, or packing different types of members in a struct.

Implemented by encoding values in mesh data, which can be passed through a node tree as geometry or object. Properties of the "struct" can be unpacked again with a dedicated node.

Node structs can be generated from existing python types. This includes the ability to define types dynamically in addons.