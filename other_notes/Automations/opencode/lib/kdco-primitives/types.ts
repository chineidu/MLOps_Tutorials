/**
 * Shared types for kdco registry plugins.
 *
 * @module kdco-primitives/types
 */

import type { OpenCode } from "@opencode/client"

/**
 * OpenCode client instance type.
 * Derived from the factory function return type for type safety.
 */
export type OpencodeClient = ReturnType<typeof OpenCode.make>
